import os
import platform
import shutil

from silly_db.helpers import set_executable
from silly_db import __version__

from flamewok.cli import cli


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()
this_os = platform.system()


plop_help = """
PLOP
Provide a Local Operationnal Pack

To get a starter pack in the current working directory:

$ silly-db plop db

provides:
- a 'database' directory containing:
    - a 'migrations' directory containing 2 examples: inital.sql, populate.sql
- a 'main_example.py' that could be a starting point for your project.
"""


def display_plop_help(*args):
    print(plop_help)


def get_db(*args):
    """Copy a starter kit in the working directory in a more convenient
    way for work"""
    shutil.copy(BASE_DIR+'/plop/db/main_example.py', cwd)
    shutil.copytree(
        BASE_DIR+'/plop/db/database', os.path.join(cwd, "database"))
    print("files successfully acquired")
    # if not running windows, set executable:
    if not this_os.lower().startswith("w"):
        set_executable(os.path.join(cwd, 'main_example.py'))


def cmd():
    cli.route(
        "HELP :",
        ("", cli.help, "display this help"),
        ("-h", cli.help, "idem"),
        ("--help", cli.help, "idem"),
        "PLOP :",
        ("plop", display_plop_help, "About plop"),
        ("plop db", get_db,
            "get a starter pack in the current working directory"),
        "_"*60,
        "ABOUT:",
        "package: silly-db",
        f"version: {__version__}",
        "description: Very light ORM for SQLite, simple and efficient",
        "home page: https://github.com/byoso/silly_db/",
    )


if __name__ == "__main__":
    cmd()
