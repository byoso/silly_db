#! /usr/bin/env python3
# coding: utf-8

from silly_db.db import DB

db = DB(file='my_db.sqlite3', initial_sql="structure_my_db.sqlite3.sql")
query = db.select(
    "* FROM cat JOIN person ON cat.owner_id=person.id WHERE cat.owner_id=1")


cat = db.select(
    "cat.name as cat, person.name as owner from cat JOIN"
    " person where cat.id=2")
print(f"cat : {cat}")
print(f"cat.exists() : {cat.exists()}")
print(cat)
print(dict(cat.items[0]))

cats = db.select(
    "cat.name as cat, person.name as owner FROM cat JOIN person ON "
    "cat.owner_id=person.id WHERE cat.owner_id=1")
print(cats.exists())
print("Jsonified cats:")
json_cats = cats.jsonify()
print(f"{json_cats}")
print(f"owner : {json_cats[0]['owner']}")


cat = db.select("* FROM cat where id=18")
print(f"cat : {cat}")
print(f"cat.exists() : {cat.exists()}")

new_selection = cat + cats
print("new: ", new_selection)
