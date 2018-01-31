import os
from string import Template

## https://nbformat.readthedocs.io/en/latest/api.html
import nbformat as nbf

from ..manager import Manager


__author__ = "John Muchovej"
__maintainer__ = "SIGAI@UCF"


class Notebooks(Manager):
    def __init__(self, gen):
        Manager.__init__(self, gen)

    def new(self):
        super().new()

    def update(self):
        super().update()

    def _build(self):
        attnd, coord = self._read_admin()
        sched = self._read_sched()
        footr = self._read_footr()

        cnt = 0

        for u in sched:
            footr_dict = {"unit_num": int(u["unit"]), "unit_nam": u["name"]}
            for m in u["list"]:
                dated = self._gen_date(m["date"], "%b %d, %Y")
                footr_dict["attnd"] = attnd
                footr_dict["dated"] = dated

                nb_name = self.gen_path + self._gen_titles(cnt, m)

                if self.type == Manager.UPDATE:
                    for filename in os.listdir(self.gen_path):
                        if filename.startswith(str(cnt).zfill(2)):
                            os.rename(self.gen_path + filename,
                                      os.path.abspath(nb_name))
                            break

                if self.type == Manager.UPDATE:
                    ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.read
                    nb = nbf.read(nb_name, as_version=4)
                elif self.type == Manager.NEW:
                    ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_notebook
                    nb = nbf.v4.new_notebook()

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#top-level-structure
                nb["metadata"]["livereveal"] = dict(
                    # autolaunch=True,
                    scroll = True,
                    footer = footr.safe_substitute(footr_dict),
                )

                ## https://nbformat.readthedocs.io/en/latest/format_description.html#notebook-metadata
                if "inst" in m and not ("Guest" in m["inst"]):
                    nb["metadata"]["authors"] = [dict(
                        name   = coord[git],
                        github = git
                    ) for git in m["inst"]]

                if self.type == Manager.NEW:
                    metadata = dict(name=m["name"], title=True)
                    title_as = "# {}\n---".format(m["name"])

                    ## https://nbformat.readthedocs.io/en/latest/api.html#nbformat.v4.new_markdown_cell
                    name = nbf.v4.new_markdown_cell(title_as, metadata=metadata)
                    nb["cells"].append(name)

                    with open(nb_name, "w") as _:
                        nbf.write(nb, _)

                cnt += 1

    def _read_footr(self):
        ## Open the Footer HTML template, we'll use this to actually build and implement all the footers
        with open(self.adm_path + "footer.html", "r") as _:
            footer_tmpl = Template(_.read())

        return footer_tmpl