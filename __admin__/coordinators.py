import yaml
from string import Template

class Coordinators:

    def __init__(self, gen):
        funcs = {
            "new"   : self._new,
            "update": self._update,
        }

        self.paths = gen.get("path")
        funcs[gen.get("type")]()

    def _new(self):
        ## Open the Admin YAML file, which contains coordinators, among other things.
        with open("{0}__admin__.yml".format(self.paths["semester"]), "r") as _:
            admin  = yaml.load(_)
            ## Grab the coordinators, we'll use this in a sec
            coords = admin["coords"]

        ## Open the Coordinator HTML template, we'll use this to actually build the cards
        with open("{0}coordinators.html".format(self.paths["components"]), "r") as _:
            coord_tmpl = Template(_.read())

        coords = [coord_tmpl.safe_substitute(dict(nam=c["nam"], git=c["git"], pos=c["pos"])) for c in coords]

        ## Build the renderable HTML
        render  = '''<h1 style="text-align: center;"> Coordinators </h1> <br> \n'''
        render += '''<div class="row"> \n'''
        render += "\n".join(coords)
        render += '''</div>'''

        print("---- Done generating from template: `coordinators.html` ----")

        ## Write Coordinators to HTML file to be rendered in Jupyter Notebooks
        with open("{0}coordinators.html".format(self.paths["semester"]), "w") as _:
            _.write(render)

        print("---- Done writing `coordinators.html` ----")

        pass

    def _update(self):
        print("Due to the nature of `coordinators.html`, we'll just overwrite the previous file.")
        self.__new()
        pass
