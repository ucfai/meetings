import re
import os
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
            "new"   : self._new,
            "update": self._update,
        }

        self.paths = gen.get("path")
        funcs[gen.get("type")]()

    def _new(self):
        ## Open the Admin YAML file, which contains the semester's attendance url
        with open("{0}__admin__.yml".format(self.paths["semester"]), "r") as _:
            admin = yaml.load(_)
            attend_url = admin["attend_url"]
            coords = {c["git"]: c["nam"] for c in admin["coords"]}

        ## Open the Schedule YAML file, which contains the semester's schedule
        with open("{0}__schedule__.yml".format(self.paths["semester"]), "r") as _:
            sched = yaml.load(_)

        ## Open the Footer HTML template, we'll use this to actually build and implement all the footers
        with open("{0}footer.html".format(self.paths["components"]), "r") as _:
            footer_tmpl = Template(_.read())

        cnt = 0

        for unit in sched:
            u = int(unit["unit"])   ## get the unit number
            n = unit["name"]       ## get the unit name
            for meet in unit["list"]:
                ## build the date
                yr = "20" + self.paths["semester"][2:-1]; mo = meet["date"][:2]; dt = meet["date"][3:]
                date = datetime.date(int(yr), int(mo), int(dt)).strftime("%b %d, %Y")
                foot_content = dict(lec_unit_num=u, lec_unit_nam=n, attend_url=attend_url, date=date)

                nb_name = Notebooks.generate_titles(self.paths["semester"], cnt, meet["type"], meet["name"])

                ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_notebook
                nb = nbf.v4.new_notebook()

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#top-level-structure
                nb["metadata"]["livereveal"] = dict(
                    # autolaunch=True,
                    scroll=True,
                    footer=footer_tmpl.safe_substitute(foot_content),
                )

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
                if "inst" in meet and not ("Guest" in meet["inst"]):
                    nb["metadata"]["authors"] = [dict(name=coords[git], github=git) for git in meet["inst"]]

                ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_markdown_cell
                name = nbf.v4.new_markdown_cell("# {}\n---".format(meet["name"], metadata=dict(name=meet["name"], title=True)))
                nb["cells"].append(name)

                with open(nb_name, "w") as _:
                    nbf.write(nb, _)

                cnt += 1

        pass

    def _update(self):
        ## Open the Admin YAML file, which contains the semester's attendance url
        with open("{0}__admin__.yml".format(self.paths["semester"]), "r") as _:
            admin = yaml.load(_)
            attend_url = admin["attend_url"]
            coords = {c["git"]: c["nam"] for c in admin["coords"]}

        ## Open the Schedule YAML file, which contains the semester's schedule
        with open("{0}__schedule__.yml".format(self.paths["semester"]), "r") as _:
            sched = yaml.load(_)

        ## Open the Footer HTML template, we'll use this to actually build and implement all the footers
        with open("{0}footer.html".format(self.paths["components"]), "r") as _:
            footer_tmpl = Template(_.read())

        cnt = 0
        cwd = os.getcwd()

        for unit in sched:
            u = int(unit["unit"])   ## get the unit number
            n = unit["name"]       ## get the unit name
            for meet in unit["list"]:
                ## build the date
                yr = "20" + self.paths["semester"][2:-1]; mo = meet["date"][:2]; dt = meet["date"][3:]
                date = datetime.date(int(yr), int(mo), int(dt)).strftime("%b %d, %Y")
                foot_content = dict(lec_unit_num=u, lec_unit_nam=n, attend_url=attend_url, date=date)

                nb_name = Notebooks.generate_titles(self.paths["semester"], cnt, meet["type"], meet["name"])
                for filename in os.listdir(self.paths["semester"]):
                    if filename.startswith(str(cnt).zfill(2)):
                        os.rename("/notebooks/{}/{}".format(self.paths["semester"], filename), os.path.abspath(nb_name))
                        break

                ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.read
                nb = nbf.read(nb_name, as_version=4)

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#top-level-structure
                nb["metadata"]["livereveal"] = dict(
                    # autolaunch=True,
                    scroll=True,
                    footer=footer_tmpl.safe_substitute(foot_content),
                )

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
                if "inst" in meet and not ("Guest" in meet["inst"]):
                    nb["metadata"]["authors"] = [dict(name=coords[git], github=git) for git in meet["inst"]]

                cnt += 1


        pass

    @staticmethod
    def generate_titles(sem, cnt, type, name, ext="ipynb"):
        ## template name for the notebooks in a given semester
        nb_tmpl = Template("${sem}/${cnt}-${type}-${name}")

        nb_meta = dict(
            sem  = sem,
            cnt  = str(cnt).zfill(2),
            type = type.lower()[:3],
            name = "-".join(re.findall(r"\w+", name.lower())),
        )

        return "{}{}".format(nb_tmpl.safe_substitute(nb_meta), "" if ext == "html" else "." + ext)
