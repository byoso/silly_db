import sys

help = """
Silly DB v1.0.6.2

more informations here:
https://github.com/byoso/silly_db/

Get some ready to use templates with 'plop'
Read the plop's help with this command line:

python3 -m silly_db.plop

"""


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(help)
