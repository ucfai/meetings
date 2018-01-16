import yaml
from string import Template
import datetime

from notebooks import Notebooks as nb

unit_tmpl = Template("""
<div class="alert alert-dark">
  <h4 class="alert-heading"> Unit $unit: $name </h4>
  <p> $desc </p>
  <div class="list-unstyled">
    $meets
  </div>
</div>
""")

meet_tmpl = Template("""
    <div class="media py-3 border border-bottom-0 border-right-0 border-left-0 border-dark">
      <a href="/meetings/$title/">
        <img src="/assets/images/$title.png">
      </a>
      <div class="media-body">
        <div class="d-flex flex-md-row justify-content-between mb-3">
          <a class="media-heading my-auto" href="/meetings/$title/"> <h5> $name </h5> </a>
          <div class="btn-toolbar">
            <div class="btn-group btn-group-sm ml-md-2">
              <span class="btn btn-info"> $date </span>
            </div>
            <div class="btn-group btn-group-sm ml-md-2">
              <span class="btn btn-warning"> $type </span>
            </div>
            <div class="btn-group btn-group-sm ml-md-2">
              $inst
            </div>
          </div>
        </div>
        <a href="/meetings/$title/">
          <p> $desc </p>
        </a>
      </div>
    </div>""")

inst_tmpl = Template("<a class=\"btn btn-dark\" href=\"https://github.com/$git/\"> $git </a>")

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
        cnt = 0
        ## Build the renderable HTML
        for u in sched:
            meets = ""
            for m in u["list"]:
                yr = "20" + self.paths["semester"][2:-1]
                mo = m["date"][:2]
                dt = m["date"][3:]
                date = datetime.date(int(yr), int(mo), int(dt)).strftime("%b %d")

                inst = []
                if "inst" in m and not ("Guest" in m["inst"]):
                    inst = [inst_tmpl.safe_substitute(git=git) for git in m["inst"]]
                    inst = "".join(inst)

                subs = dict(
                    date  = date,
                    inst  = inst,
                    desc  = m["desc"],
                    name  = m["name"],
                    type  = m["type"],
                    sem   = self.paths["semester"][:-1],
                    title = nb.generate_titles(
                        cnt  = cnt,
                        ext  = "html",
                        name = m["name"],
                        type = m["type"],
                        sem  = self.paths["semester"][:-1],
                    ))

                meets += meet_tmpl.safe_substitute(subs)

                cnt += 1

            render += unit_tmpl.safe_substitute(dict(unit=u["unit"], name=u["name"], desc=u["desc"], meets=meets))

        ## Open the Syllabus component (this has the wrapper HTML for the table)
        with open(self.paths["components"] + "syllabus.html", "r") as _:
            syll = Template(_.read())

        print("---- Done generating from template: `syllabus.html` ----")

        ## Write Syllabus to HTML file to be rendered in Jupyter Notebooks
        with open("{0}syllabus.html".format(self.paths["semester"]), "w") as _:
            _.write(syll.safe_substitute(dict(syllabus=render)))

        print("---- Done writing `syllabus.html` ----")

        pass

    def _update(self):
        print("Due to the nature of `syllabus.html`, we'll just overwrite the previous file.")
        self._new()
        pass
