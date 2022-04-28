import sys
import os
import shutil


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
- an example of what could do a main.py file do with the database created
"""

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_db():
    cwd = os.getcwd()
    shutil.copy(BASE_DIR+'/db/database.py', cwd)
    shutil.copy(BASE_DIR+'/db/migrator.py', cwd)
    shutil.copy(BASE_DIR+'/db/main_example.py', cwd)
    shutil.copytree(BASE_DIR+'/db/migrations', os.path.join(cwd, "migrations"))
    print("files successfully acquired")


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
