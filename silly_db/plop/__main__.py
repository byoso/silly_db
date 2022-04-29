import sys
import os
import platform
import shutil

from silly_db.helpers import set_executable


help = """
PLOP
Provide a Local Operationnal Pack

'python3 -m silly_db.plop [option]'

options are:

[tuto]
provides in your working directory:
- a basic 'database.py' template
- a basic 'migrator.py' template
- a 'migrations' directory containing 2 examples: inital.sql, populate.sql
- a 'main_example.py' that is showing a few examples and could be a
    starting point for your project.

[db]
provides the same as tuto but packaged into a directory:
- a 'database' directory containing:
    - a basic 'database.py' template
    - a basic 'migrator.py' template
    - a 'migrations' directory containing 2 examples: inital.sql, populate.sql
- a 'main_example.py' that is showing a few examples and could be a
    starting point for your project.
"""

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()
this_os = platform.system()


def get_tuto():
    """Copy a starter tutorial kit files to the working directory"""
    shutil.copy(BASE_DIR+'/tuto/database.py', cwd)
    shutil.copy(BASE_DIR+'/tuto/migrator.py', cwd)
    shutil.copy(BASE_DIR+'/tuto/main_example.py', cwd)
    shutil.copytree(
        BASE_DIR+'/tuto/migrations', os.path.join(cwd, "migrations"))
    print("files successfully acquired")
    # if not running windows, set executable:
    if not this_os.lower().startswith("w"):
        set_executable(os.path.join(cwd, 'migrator.py'))
        set_executable(os.path.join(cwd, 'main_example.py'))


def get_db():
    """Copy a starter kit in the working directory in a more convenient
    way for work"""
    shutil.copy(BASE_DIR+'/db/main_example.py', cwd)
    shutil.copytree(
        BASE_DIR+'/db/database', os.path.join(cwd, "database"))
    print("files successfully acquired")
    # if not running windows, set executable:
    if not this_os.lower().startswith("w"):
        set_executable(os.path.join(cwd, 'database/migrator.py'))
        set_executable(os.path.join(cwd, 'main_example.py'))


options = {
    'db': get_db,
    'tuto': get_tuto,
}


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(help)

    if len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        if arg not in options:
            print("invalid option given to silly_db.plop")
            print(help)
        else:
            options[arg]()
