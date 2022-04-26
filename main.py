#! /usr/bin/env python3
# coding: utf-8


from database import db
from silly_db.helpers import text


# db.execute("INSERT INTO 'person' ('name', 'age') VALUES('Jean', 32);")
# db.execute("INSERT INTO cat (name, owner_id) VALUES('Bouton d''or', 4)")
name = text("bouton d'or")
db.execute(f"INSERT INTO cat (name, owner_id) VALUES('{name}', 4);")
persons = db.select("* from person")
cats = db.select("* from cat")
for person in persons:
    print(f"name: {person.name} - age: {person.age}")
print([cat.name for cat in cats])
print(cats.jsonify())
