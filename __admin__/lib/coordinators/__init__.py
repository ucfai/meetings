from string import Template

from ..manager import Manager

class Coordinators(Manager):
    def __init__(self, gen):
        self.file_path = "assets/coordinators.html"
        super().__init__(gen)

    def new(self):
        super().new()

    def update(self):
        print("Due to the nature of `{}`, we'll just overwrite "
              "the previous file.".format(self.file_path))
        super().update()

    def _build(self):
        _, coords = self._read_admin()

        ## Open the Coordinator HTML template, we'll use this to actually build the cards
        with open(self.adm_path + "coordinators.html", "r") as _:
            coord = Template(_.read())

        coords = [ coord.safe_substitute({ "nam": val[0],
                                           "git": key,
                                           "pos": val[1], }) for key, val in coords.items() ]

        ## Build the renderable HTML
        render  = '''<div class="row"> \n'''
        render += "\n".join(coords)
        render += '''</div>'''

        print("---- Done generating from template: `{}` ----".format(self.file_path))

        ## Write Coordinators to HTML file to be rendered in Jupyter Notebooks
        with open(self.gen_path + self.file_path, "w") as _:
            _.write(render)

        print("---- Done writing: `{}` ----".format(self.file_path))
