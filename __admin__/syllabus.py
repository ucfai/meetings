import yaml
from string import Template
import datetime

unit_tmpl = Template("        <tr class=\"syllabus-unit-title\">\n" + \
                     "          <td colspan=\"4\">Unit $unit: $name </td>\n" + \
                     "        </tr>\n")

meet_tmpl = Template("        <tr>\n" + \
                     "          <td> $type </td>\n" + \
                     "          <td> $date </td>\n" + \
                     "          <td> $name </td>\n" + \
                     "          <td> $inst </td>\n" + \
                     "        </tr>\n")

meet_inst_tmpl = Template("<a href=\"https://github.com/$git/\"> $git </a>")

class Syllabus:

    def __init__(self, gen):
        funcs = {
            "new"   : self._new,
            "update": self._update,
        }

        self.paths = gen.get("path")
        funcs[gen.get("type")]()

    def _new(self):
        ## Open the Schedule YAML file, which contains the semester's lectures/workshops
        with open(self.paths["semester"] + "__schedule__.yml", "r") as _:
            sched = yaml.load(_)

        render = ""
        ## Build the renderable HTML
        for u in sched:
            render += unit_tmpl.safe_substitute(dict(unit=u["unit"], name=u["name"]))
            for m in u["list"]:
                yr = "20" + self.paths["semester"][2:-1]
                mo = m["date"][:2]
                dt = m["date"][3:]
                date = datetime.date(int(yr), int(mo), int(dt)).strftime("%b %d")

                inst = []
                if "inst" in m and not ("Guest" in m["inst"]):
                    inst = [meet_inst_tmpl.safe_substitute(git=git) for git in m["inst"]]
                    inst = ", ".join(inst)

                subs = dict(type=m["type"], date=date, name=m["name"], inst=inst)
                render += meet_tmpl.safe_substitute(subs)

        ## Open the Syllabus component (this has the wrapper HTML for the table)
        with open(self.paths["components"] + "syllabus.html", "r") as _:
            syll = Template(_.read())

        print("---- Done generating from template: `syllabus.html` ----")

        ## Write Syllabus to HTML file to be rendered in Jupyter Notebooks
        with open("{0}syllabus.html".format(self.paths["semester"]), "w") as _:
            _.write(syll.safe_substitute(dict(tbody=render)))

        print("---- Done writing `syllabus.html` ----")

        pass

    def _update(self):
        print("Due to the nature of `syllabus.html`, we'll just overwrite the previous file.")
        self.__new()
        pass
