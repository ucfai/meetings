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

class Notebooks:

    def __init__(self, gen):
        funcs = {
            "new"   : self.__new,
            "update": self.__update,
        }

        self.paths = gen.get("path")
        funcs[gen.get("type")]()

    def _new(self):
        ## Open the Schedule YAML file, which contains the semester's schedule
        with open("{0}__schedule__.yml".format(self.semester), "r") as _:
            sched = yaml.load(_)

        ## Open the Footer HTML template, we'll use this to actually build and implement all the footers
        with open("{0}footer.html".format(self.components_path), "r") as _:
            footer_tmpl = Template('''{}'''.format(_.read()))

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
                    scroll=True,
                    footer=footer_tmpl.safe_substitute(foot_content),
                )

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
                if "inst" in meet:
                    nb["metadata"]["authors"] = [dict(name=cords[git], github=git) for git in meet["inst"]]

                ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_markdown_cell
                name = nbf.v4.new_markdown_cell("# {}\n---".format(meet["name"], metadata=dict(name=meet["name"])))
                nb["cells"].append(name)

                nb_meta = dict(
                    sem=self.semester,
                    nb_cont=str(cnt).zfill(2),
                    nb_type=meet["type"].lower()[:3],
                    nb_name="-".join(re.findall(r"\w+", meet["name"].lower())),
                )
                with open(nb_tmpl.substitute(nb_meta), "w") as _:
                    nbf.write(nb, _)

                cnt += 1
        pass

    def _update(self):
        ## Open the Schedule YAML file, which contains the semester's schedule
        with open("{0}__schedule__.yml".format(self.semester), "r") as _:
            sched = yaml.load(_)

        ## Open the Footer HTML template, we'll use this to actually build and implement all the footers
        with open("{0}footer.html".format(self.components_path), "r") as _:
            footer_tmpl = Template(_.read())

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

                nb_meta = dict(
                    sem=self.semester,
                    nb_cont=str(cnt).zfill(2),
                    nb_type=meet["type"].lower()[:3],
                    nb_name="-".join(re.findall(r"\w+", meet["name"].lower())),
                )

                ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.read
                nb = nbf.v4.read(nb_tmpl.substitute(nb_meta))


                ## https://nbformat.readthedocs.io/en/latest/format_description.html#top-level-structure
                nb["metadata"]["livereveal"] = dict(
                    autolaunch=True,
                    scroll=True,
                    footer=footer_tmpl.safe_substitute(foot_content),
                )

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
                if "inst" in meet:
                    nb["metadata"]["authors"] = [dict(name=cords[git], github=git) for git in meet["inst"]]

                ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_markdown_cell
                name = nbf.v4.new_markdown_cell("# {}\n---".format(meet["name"], metadata=dict(name=meet["name"])))
                nb["cells"].append(name)

                with open(nb_tmpl.substitute(nb_meta), "w") as _:
                    nbf.write(nb, _)

                cnt += 1
        pass
