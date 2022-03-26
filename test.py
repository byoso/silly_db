#! /usr/bin/env python3
# coding: utf-8


from sillydb.db import ModelTable, ModelDB



db = ModelDB()


persons = ModelTable(
    fields=["name", "age"],
)

cats = ModelTable(
    fields=["name", ],
)


db.add_tables([persons, cats])

persons.create("Vincent", "45")
persons.create("Vic", "35")
persons.create("Gordon", "52")
persons.create("Micheline", "23")
persons.create("Jayna", "38")
persons.create("Chloê", "19")
persons.create("Joe",)
persons.create(age="77")
liste_persons = persons.all()
print(liste_persons)


one_is = persons.filter("id", 1)
print(one_is)

persons.delete(3)
print(persons.all())

print(f"id6: {persons.get(6)}")

# print(persons)
print(db)
