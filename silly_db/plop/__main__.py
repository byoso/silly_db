import sys
import os
import platform
import shutil

from silly_db.helpers import set_executable


help = """
PLOP
Provide a Local Operationnal Pack

'python3 -m silly_db.plop [option]' will provide some files in your
working directory:

options are:

db
provides:
- a basic 'database.py' template
- a basic 'migrator.py' template
- a 'migrations' directory containing 2 examples: inital.sql, populate.sql
- an 'main_example.py' that is showing a few examples and could be a
    starting point for your project.
"""

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_db():
    """Copy a starter kit files to the working directory"""
    cwd = os.getcwd()
    shutil.copy(BASE_DIR+'/db/database.py', cwd)
    shutil.copy(BASE_DIR+'/db/migrator.py', cwd)
    shutil.copy(BASE_DIR+'/db/main_example.py', cwd)
    shutil.copytree(BASE_DIR+'/db/migrations', os.path.join(cwd, "migrations"))
    print("files successfully acquired")
    # if not running windows, set executable:
    this_os = platform.system()
    if not this_os.lower().startswith("w"):
        set_executable(os.path.join(cwd, 'migrator.py'))
        set_executable(os.path.join(cwd, 'main_example.py'))


options = {
    'db': get_db,
}


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(help)

    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        if arg not in options:
            print("invalid option")
            print(help)
        else:
            options[arg]()
