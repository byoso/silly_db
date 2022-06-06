![logo silly db](https://i.goopics.net/60cef4.png)

# Silly DB
*Quick and easy SQLite ORM  for local python applications.*

## Is it really an ORM ?
It is indeed a ***reversed*** ORM:

- The structure of the DB is built from classic .sql files.
- Then the magic occures to get the models **from** the DB itself. Usually, an ORM does the contrary.

Some minimum SQL knowledge **is required**, the purpose of Silly DB is not to get rid of SQL (actualy, SQL is the best language to manage... a SQL database), but to handle the annoying things, and let you focus on your application with a minimum amount of code.

## Installation

```
$ pip install silly-db
```

## Fast way to begin

Create a new directory and open a console in there.

Get a basic working structure with 'plop':
```
$ silly-db plop db
```

Congratulations ! You've got your database ready to work !
To understand how it works, open the differents files provided and read the comments, it will be easy to adapt to your own needs.

get more info with:
```
$ silly-db -h
```
and more about the plop options here:
```
$ silly-db plop
```

## Examples (simple CRUD)

```python

Cat = db.model('cat') # model created from the existing database

Cat.insert(name="Kutty", owner_id=1)
cats = Cat.filter("name like 'K%'")
print(cats.jsonify())

>>>[{'id': 58, 'name': 'Kutty', 'owner_id': 1}]

Cat.update("id=58", name="Duke")
cat = cat.get("id=58")
print(cat.name)
>>> 'Duke'

print(cat.jsonify())
>>>{'id': 58, 'name': 'Duke', 'owner_id': 1}

cat.delete("id=58")

```

## Documentation
Take a look at the [wiki here](https://github.com/byoso/silly_db/wiki#silly-db-wiki)