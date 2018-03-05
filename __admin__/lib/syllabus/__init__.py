from string import Template

from ..manager import Manager
from ..notebooks import Notebooks


class Syllabus(Manager):
    def __init__(self, gen):
        super().__init__(gen)

    def new(self):
        super().new()

    def update(self):
        print("Due to the nature of `syllabus/page.html`, we'll just overwrite "
              "the previous file.")
        super().update()

    def _build(self):
        with open(self.adm_path + "unit.html", "r") as _:
            unit_tmpl = Template(_.read())

        with open(self.adm_path + "meet.html", "r") as _:
            meet_tmpl = Template(_.read())

        with open(self.adm_path + "inst.html", "r") as _:
            inst_tmpl = Template(_.read())

        sched = super()._read_sched()

        render = ""
        cnt = 0
        # Build the renderable HTML
        for u in sched:
            meets = ""
            for m in u["list"]:
                date = self._gen_date(m["date"], "%b %d")

                inst = []
                if "inst" in m and "Guest" not in m["inst"]:
                    inst = [inst_tmpl.safe_substitute(git=git)
                            for git in m["inst"]]
                    inst = "".join(inst)

                subs = dict(
                    date  = date,
                    inst  = inst,
                    desc  = m["desc"],
                    name  = m["name"],
                    type  = m["type"],
                    sem   = self.sem,
                    title = self._gen_titles(
                        cnt  = cnt,
                        ext  = "html",
                        meet = m,
                    ),
                    fb    = self._gen_fburl(m["fb"]),
                    yt    = self._gen_yturl(m["yt"]),
                )

                type_html = "<i class=\"far fa-{}\"></i>".format(
                    "sticky-note" if m["type"] == "Lecture" else "keyboard")
                subs["type"] = "{1}\n{0}".format(m["type"], type_html)

                meets += meet_tmpl.safe_substitute(subs)

                cnt += 1

            render_tmp = dict(unit=u["unit"], name=u["name"],
                              desc=u["desc"], meets=meets)
            render += unit_tmpl.safe_substitute(render_tmp)

        # Open the Syllabus component (this has the wrapper HTML for the table)
        with open(self.adm_path + "page.html", "r") as _:
            syll = Template(_.read())

        print("---- Done generating from template: `syllabus/page.html` ----")

        # Write Syllabus to HTML file to be rendered in Jupyter Notebooks
        with open(self.gen_path + "assets/syllabus.html", "w") as _:
            _.write(syll.safe_substitute(dict(syllabus=render)))

        print("---- Done writing `syllabus/page.html` ----")
