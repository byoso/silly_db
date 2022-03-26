#! /usr/bin/env python3
# coding: utf-8


from sillydb.db import ModelTable, ModelDB



db = ModelDB()


persons = ModelTable(
    fields=[
        "name",
        "age",
        ],
)

cats = ModelTable(
    fields=[
        "name",
        ],
)


db.add_tables([persons, cats])

persons.create("Vincent", "45")
persons.create("Vic", "35")
persons.create("Gordon", "52")
persons.create("Micheline", "23")
persons.create("Jayna", "32")
persons.create("Chloê", "19")
persons.create("Joe", "12")
persons.create(str(), int())
liste_persons = persons.all()



one_is = persons.all().id_get(3)
print(one_is)

persons.delete(3)
print(persons.all())

print(f"id6: {persons.get(6)}")

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

print(f"everyone sorted : {everyone.sort_by('-name')}")
