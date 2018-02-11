import re
import abc
from string import Template

## https://github.com/yaml/pyyaml
import yaml

import datetime


REQD_FILES = sorted(["__admin__.yml", "__sched__.yml"])


class Manager(metaclass=abc.ABCMeta):
    UPDATE = "update"
    NEW = "new"

    def __init__(self, gen):
        funcs = {
            Manager.NEW:    self.new,
            Manager.UPDATE: self.update,
        }

        self.sem = gen["path"]["semester"]
        self.name = type(self).__name__.lower()
        self.adm_path = "/notebooks/__admin__/lib/" + self.name + "/"
        self.gen_path = "/notebooks/" + self.sem + "/"
        self.type = gen["type"]

        self.yml = {key[2:7]: "{}{}".format(self.gen_path, key)
                    for key in REQD_FILES}

        funcs[gen["type"]]()

    @abc.abstractmethod
    def new(self):
        """This method handles the creation of new elements for a
        given semester.
        """
        self.type = Manager.NEW
        self._build()

    @abc.abstractmethod
    def update(self):
        """This method handles the updating of elements for a given semester,
        provided it's been created.
        """
        self.type = Manager.UPDATE
        self._build()

    @abc.abstractmethod
    def _build(self):
        """This method handles the updating of elements for a given semester,
        provided it's been created.
        """
        pass

    def _gen_date(self, date, fmt):
        return datetime.date(int("20" + self.sem[2:-1]), int(date[:2]),
                             int(date[3:])).strftime(fmt)

    def _read_admin(self):
        ## Open the Admin YAML file
        with open(self.yml["admin"], "r") as _:
            admin = yaml.load(_)
            attend_url = admin["attend_url"]
            coords = {c["git"]: (c["nam"], c["pos"]) for c in admin["coords"]}

        return attend_url, coords

    def _read_sched(self):
        ## Open the Schedule YAML file, which contains the semester's schedule
        with open(self.yml["sched"], "r") as _:
            sched = yaml.load(_)

        return sched

    def _gen_titles(self, cnt, meet, ext="ipynb"):
        ## template name for the notebooks in a given semester
        nb_tmpl = Template("${cnt}-${type}-${name}")

        nb_meta = dict(
            cnt  = str(cnt).zfill(2),
            type = meet["type"].lower()[:3],
            name = "-".join(re.findall(r"\w+", meet["name"].lower())),
        )

        ext_use  = "" if ext == "html" else "." + ext
        return nb_tmpl.safe_substitute(nb_meta) + ext_use

    def _gen_fburl(self, fb):
        return "" if str(fb) == "" else ("https://fb.com/events/" + str(fb))

    def _gen_yturl(self, yt):
        return "" if str(yt) == "" else ("https://youtu.be/" + str(yt))
