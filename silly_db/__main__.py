import sys

help = """
Silly db

more informations here:
https://github.com/byoso/silly_db/

Get some templates with plop
To read the plop help use this command line:

python3 -m silly_db.plop


"""


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(help)
