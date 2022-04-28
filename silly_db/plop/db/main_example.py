#! /usr/bin/env python3
# coding: utf-8

"""Example of an embryonic main.py file"""

from database import db
from silly_db.helpers import text


# AT FIRST:
# Do not forget to run the migrator.py once, to create the database.
# Take a look into the migrator.py and database.py, it is very simple
# to adapt this code to your own needs.


# SOME TIPS :

# If a text that you want to insert in your database may contain quotes,
# use the helper text():
name = text("bouton d'or")
db.execute(f"INSERT INTO cat (name, owner_id) VALUES('{name}', 4);")

# a Selection is iterable:
persons = db.select("* from person")
for person in persons:
    print(f"name: {person.name} - age: {person.age}")

# it can also be jsonified:
cats = db.select("* from cat")
print([cat.name for cat in cats])
print(cats.jsonify())

# Avoid ambiguous headers (column names):
cats2 = db.select(
    "cat.name as pet, person.name as owner FROM cat JOIN person ON "
    "cat.owner_id=person.id"
    )
print(cats2.jsonify())
