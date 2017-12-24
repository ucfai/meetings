import re
import sys
from string import Template
import datetime

## https://github.com/yaml/pyyaml
import yaml

## https://nbformat.readthedocs.io/en/latest/api.html
import nbformat as nbf


__author__ = "John Muchovej"
__maintainer__ = "SIGAI@UCF"



class Semester:
    def __init__(self, semester):
        self.components_path = ".scripts/components/"
        self.semester = semester + "/"
        pass


    def new(self):
        ## Open the Admin YAML file, which contains coordinators, among other things.
        with open("{0}__admin__.yml".format(self.semester), "r") as admin_yml:
            ## Open the Coordinator HTML template, we'll use this to actually build the cards
            with open("{0}coordinators.html".format(self.components_path), "r") as coord:
                coord_tmpl = Template('''{}'''.format(coord.read()))
                ## Grab the attendance URL, we'll need it for building the footer
                ## Grab the coordinators, we'll use this right now
                admin = yaml.load(admin_yml); attend_url = admin["attend_url"]; coords = admin["coords"]
                cords = {c["git"]: c["nam"] for c in coords}
                coords = [coord_tmpl.safe_substitute(dict(nam=c["nam"], git=c["git"], pos=c["pos"])) for c in coords]

                ## Build the renderable HTML
                render  = '''<h1 style="text-align: center;"> Coordinators </h1> <br> \n'''
                render += '''<div class="row"> \n'''
                render += "\n".join(coords)
                render += '''</div>'''

                coord.close()

            ## Write Coordinators to HTML file to be rendered in Jupyter Notebooks
            with open("{0}coordinators.html".format(self.semester), "w") as this_sem_coords:
                this_sem_coords.write(render)
                this_sem_coords.close()

            admin_yml.close()

        ## Open the Schedule YAML file, which contains the semester's schedule
        with open("{0}__schedule__.yml".format(self.semester), "r") as sched_yml:
            ## Open the Footer HTML template, we'll use this to actually build and implement all the footers
            with open("{0}footer.html".format(self.components_path), "r") as footer:
                footer_tmpl = Template('''{}'''.format(footer.read()))
                sched = yaml.load(sched_yml)
                cnt = 0

                ## template name for the notebooks in a given semester
                nb_tmpl = Template("${sem}/${nb_cont}-${nb_type}-${nb_name}.ipynb")

                for unit in sched:
                    u = int(unit["unit"])   ## get the unit number
                    n = unit["title"]       ## get the unit name
                    for meet in unit["list"]:
                        ## build the date
                        yr = "20" + self.semester[2:-1]; mo = meet["date"][:2]; dt = meet["date"][3:]
                        date = datetime.date(int(yr), int(mo), int(dt)).strftime("%b %d, %Y")
                        foot_content = dict(lec_unit_num=u, lec_unit_nam=n, attend_url=attend_url, date=date)

                        ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_notebook
                        nb = nbf.v4.new_notebook()

                        ## https://nbformat.readthedocs.io/en/latest/format_description.html#top-level-structure
                        nb["metadata"]["livereveal"] = dict(
                            autolaunch=True,
                            footer=footer_tmpl.safe_substitute(foot_content),
                        )

                        ## https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
                        if "lecturer" in meet:
                            nb["metadata"]["authors"] = [dict(name=cords[git], github=git) for git in meet["lecturer"]]

                        ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_markdown_cell
                        nb["cells"].append(nbf.v4.new_markdown_cell("# {}\n---".format(meet["title"])))

                        nb_meta = dict(
                            sem=self.semester,
                            nb_cont=str(cnt).zfill(2),
                            nb_type=meet["type"].lower()[:3],
                            nb_name="-".join(re.findall(r"\w+", meet["title"].lower())),
                        )
                        with open(nb_tmpl.substitute(nb_meta), "w") as _:
                            nbf.write(nb, _)

                        cnt += 1

                footer.close()
            sched_yml.close()

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "new":
        sem = Semester(sys.argv[2])
        sem.new()
    else:
        raise NotImplementedError("Looks like we haven't built in that functionality yet! :/")
