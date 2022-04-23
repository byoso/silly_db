#! /usr/bin/env python3
# coding: utf-8

from silly_db.db import DB

db = DB(file='my_db.sqlite3', initial_sql="structure_my_db.sqlite3.sql")
query = db.select(
    "* FROM cat JOIN person ON cat.owner_id=person.id WHERE cat.owner_id=1")

print(query.json)
print(query.items[0].name)

cats = db.select(
    "cat.name as cat, person.name as owner from cat JOIN"
    " person where cat.id=2")
print(cats)


query2 = db.select(
    "cat.name as cat, person.name as owner FROM cat JOIN person ON "
    "cat.owner_id=person.id WHERE cat.owner_id=1")
print(query2)
print(query2.items[0].cat)
print(query2.items[1].cat)

# db.export()
