import argparse
import os

from lib.coordinators import Coordinators
from lib.notebooks import Notebooks
from lib.syllabus import Syllabus

from lib.manager import REQD_FILES

root = "/notebooks/"
path_prefix = "__admin__/"

required_files = REQD_FILES

accepted_args = sorted(["coordinators", "notebooks", "syllabus"])


class Semester:
    def __init__(self, semester):
        self.semester = semester
        self.paths = {"semester": semester}
        self.gen = {}

    def new(self, component=None, accept=False):
        self.gen["type"] = "new"
        self.gen["path"] = self.paths

        if component is None:
            if os.path.isdir(self.semester) and len(os.listdir(self.semester)) \
                    != 0:
                if not accept:
                    overwrite_warning = "You may **_overwrite_** important " \
                                        "files in `{}`. Careful. Do you wish " \
                                        "to proceed? " \
                                        "[y/N]".format(self.semester)

                    overwrite = input(overwrite_warning).lower() == "y"

            if not os.path.isdir(self.semester):
                os.path.mkdir(self.semester)
                raise OSError("{0}\n{1}\n{2}\n".format(
                    "I've just generated the `{}` directory for you. Now you "
                    "need to add two files:".format(self.semester),
                    "    1. __admin__.yml",
                    "    2. __sched__.yml"
                    )
                )

            if sorted(os.listdir(self.semester), key=str.lower) \
                    != required_files:
                raise OSError(["You're missing {0}]\n.".format(f)
                               for f in required_files])

            Syllabus(self.gen)
            Notebooks(self.gen)
            Coordinators(self.gen)
        else:
            f = "{}/{}.html".format(self.semester, component)
            print("You're trying to generate a new component for `{}`".format(f))
            components = dict(
                syllabus     = Syllabus,
                coordinators = Coordinators,
                notebooks    = Notebooks,
            )
            if component not in ["notebooks"] and os.path.isfile(f):
                if not accept:
                    overwrite = input("You're about to overwrite `{}`. Are you "
                                      "sure? [y/N] ".format(f)) == "y"

                if overwrite or accept:
                    components[component](self.gen).new()
                    print("Successfully (re)generated `{}`.".format(f))
                else:
                    print("You didn't want to overwrite anything; so I didn't. "
                          "Bye! :D")
            else:
                if not accept:
                    overwrite = input("You're about to overwrite all the "
                                      "notebooks in `{}`. Are you sure? [y/N] "
                                      "".format(self.semester)) == "y"
                if overwrite or accept:
                    components[component](self.gen).new()
                    print("Successfully (re)generated `{}`.".format(f))
                else:
                    print("You didn't want to overwrite anything; so I didn't. "
                          "Bye! :D")

    def update(self, component, accept=False):
        self.gen["type"] = "update"
        self.gen["path"] = self.paths

        if component is None:
            raise ValueError("You failed to specify a component to update. "
                             "Please try again, remember to use the `-c` flag "
                             "to specify the component.")
        elif component not in accepted_args:
            raise ValueError("You failed to specify an acceptable argument. "
                             "{}".format(accepted_args))
        else:
            components = dict(
                syllabus     = Syllabus,
                notebooks    = Notebooks,
                coordinators = Coordinators,
            )

            # if os.path.isfile(f):
            if not accept:
                overwrite = input("You're about to overwrite `{}`. Are you "
                                  "sure? [y/N] ".format(component)) == "y"

            if overwrite or accept:
                components[component](self.gen).update()
                print("Successfully (re)generated `{}`.".format(component))
            else:
                print("You didn't want to overwrite anything; so I didn't. "
                      "Bye! :D")

        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Semester setup")
    parser.add_argument("action", metavar="A", type=str,
                        help="Choose an action to do -- `new` or `update`. "
                             "`new` will wipe all data from the specified "
                             "directory if the semester has already been "
                             "initialized. Please be wary of using this.")
    parser.add_argument("semester", metavar="U", type=str,
                        help="Choose a semester, of the form: `faXX` or "
                             "`spXX`, where `fa` and `sp` are for Fall and "
                             "Spring, respectively, and `XX` should be "
                             "substituted with the last two digits of the "
                             "planned year.")
    parser.add_argument("-c", "--component", dest="component", type=str,
                        help="You should only use this when updating a "
                             "semester.")
    parser.add_argument("-y", "--yes", dest="accept", type=bool,
                        help="Automatically accept all validations. CAREFUL. "
                             "This can be VERY dangerous.")

    args = parser.parse_args()
    sem = Semester(args.semester)
    if args.action  == "new":
        sem.new(component=args.component, accept=args.accept)
    elif args.action == "update":
        sem.update(args.component, accept=args.accept)
    else:
        raise NotImplementedError("Looks like we haven't built in that "
                                  "functionality yet! :/")
