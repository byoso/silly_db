#! /usr/bin/env python3
# coding: utf-8


from sillydb.db import ModelTable, ModelDB
from sillydb.table import Field



db = ModelDB()


persons = ModelTable(
    fields=[
        Field("name", str),
        Field("age", int),
        ],
)

cats = ModelTable(
    fields=[
        Field("name", str),
        # Field("owner", FK, "cat"),  # TODO
        ],
)


db.add_tables([persons, cats])

persons.create("Vincent", 45)
persons.create("Vic", 35)
persons.create("Gordon", 52)
persons.create("Micheline", 23)
persons.create("Jayna", 32)
persons.create("Chloê", 19)
persons.create("Joe", 21)
persons.create(age=21, name="Zoé")
persons.create()
liste_persons = persons.all()

one_is = persons.all().get(id=3)
print(one_is)

persons.delete(3)
print(persons.all())

print(f"id6: {persons.get(id=6)}")

print(db)

exemptes = persons.all().filter_lambda(
    lambda x: int(x.age) <= 18 or int(x.age) >= 70)
print(f"exemptes : {exemptes}")

youngs = persons.all().filter_lambda(lambda x: int(x.age) <= 35)
olds = persons.all().filter_lambda(lambda x: int(x.age) >= 30)

everyone = youngs + olds

print(f"youngs : {youngs}")
print(f"olds : {olds}")
print(f"everyone : {everyone}")

young_again = everyone - olds
print(f"everyone but the olds : {young_again}")

both = olds & youngs
print(f"those on both: {both}")

print(f"len(both): {len(both)}")
print(f"list(both): {list(both)}")

print(f"everyone sorted : {everyone.sort_by('age')}")
print(persons.get(age=21, name="Joe"))
