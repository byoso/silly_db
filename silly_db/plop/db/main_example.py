#! /usr/bin/env python3
# coding: utf-8

"""Example of an embryonic main.py file, this should be included in
a MCV designed program"""

from silly_db.db import DB
from silly_db.helpers import to_sql

# Database initialized here
db = DB(file="database/my_db.sqlite3", migrations_dir="database/migrations")
# make migrations from the migrations_dir
db.migrate_all()


# SOME TIPS :
# to_sql cleans the data to be insertable into sql
name = to_sql("bouton d'or")  # single quote escaped
owner_id = to_sql(None)  # None becomes 'NULL'
# BEWARE: quotes around '{name}' but not around {owner_id}
db.execute(f"INSERT INTO cat (name, owner_id) VALUES('{name}', {owner_id});")

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
