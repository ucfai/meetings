from string import Template

from ..manager import Manager


class Coordinators(Manager):
    def __init__(self, gen):
        super().__init__(gen)

    def new(self):
        super().new()

    def update(self):
        print("Due to the nature of `coordinators.html`, we'll just overwrite "
              "the previous file.")
        super().update()

    def _build(self):
        _, coords = self._read_admin()

        ## Open the Coordinator HTML template, we'll use this to actually build the cards
        with open(self.adm_path + "coordinators.html", "r") as _:
            coord = Template(_.read())

        coords = [ coord.safe_substitute({ "nam": c["nam"],
                                           "git": c["git"],
                                           "pos": c["pos"], }) for c in coords ]

        ## Build the renderable HTML
        render  = '''<h1 style="text-align: center;"> Coordinators </h1> <br> \n'''
        render += '''<div class="row"> \n'''
        render += "\n".join(coords)
        render += '''</div>'''

        print("---- Done generating from template: `coordinators.html` ----")

        ## Write Coordinators to HTML file to be rendered in Jupyter Notebooks
        with open(self.gen_path + "coordinators.html", "w") as _:
            _.write(render)

        print("---- Done writing `coordinators.html` ----")
