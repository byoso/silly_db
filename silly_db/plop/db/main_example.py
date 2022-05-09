#! /usr/bin/env python3
# coding: utf-8

"""Example of an embryonic main.py file, this should be included in
a MCV designed program"""

from silly_db.db import DB

# Database initialized here
db = DB(file="database/my_db.sqlite3", migrations_dir="database/migrations")
# makes the new migrations only from the migrations_dir
db.migrate_all()

Cat = db.model('cat')
Person = db.model('person')

cats = Cat.all()
print(cats)
