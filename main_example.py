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

Cat = db.model('cat')
Person = db.model('person')

cat = Cat.get_id(1)
print(dict(cat))

cat_owner_in = cat.fusion_in("owner", Person.get_id(cat.id), "owner_id")
# cat_owner_on = cat.fusion_on(Person.get_id(cat.id), "owner_id")
print(dict(cat_owner_in))
# print(dict(cat_owner_on))
print(dict(cat))
