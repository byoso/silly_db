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
- a basic 'main.py' template
- a basic 'initial.sql' file

"""

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_db():
    cwd = os.getcwd()
    shutil.copy(BASE_DIR+'/main.py', cwd)
    shutil.copy(BASE_DIR+'/initial.sql', cwd)
    print("files successfully acquired")


options = {
    'db': get_db
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
