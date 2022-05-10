![logo silly db](https://i.goopics.net/60cef4.png)

# Silly DB
*Quick and easy SQLite database  for local python applications.*

## Is it an ORM ?
It is indeed a ***reversed*** ORM:

- The structure of the DB is built from classic .sql files.
- Then the magic occures to get the models **from** the DB itself. Usually, an ORM does the contrary.

Some minimum SQL knowledge **is required**, the purpose of Silly DB is not to get rid of SQL (actualy, SQL is the best language to manage... a SQL database), but to handle the a lot of boring things, and let you focus on your application with a minimum amount of code.

The required knowledge and much more is available here :

- [SQLite.org](https://www.sqlite.org/index.html)

You should consider using :

- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [SQLite Studio](https://sqlitestudio.pl/)

No need to be an expert, just understand own to create a DB and use 'SELECT' will be fine.

## Installation

```
$ pip install silly_db
```

## Fast way to begin

Create a new directory and open a console in there.

Get a basic working structure with 'plop':
```
$ python3 -m silly_db.plop db
```

Congratulations ! You've got your database ready to work !
To understand how it works, open the differents files provided and read the comments, it will be easy to adapt to your own needs.

get more info with:
```
$ python3 -m silly_db
```
and more about the plop options here:
```
$ python3 _n silly_db.plop
```


## Examples

```python
from silly_db.db import DB

db = DB(file="database/my_db.sqlite3", migrations_dir="database/migrations")
db.migrate_all()

Cat = db.model('cat')
Person = db.model('person')

Cat.insert(name="Kutty", owner_id=1)
cats = Cat.filter("name like 'K%'")
print(cats.jsonify())

>>>[{'id': 58, 'name': 'Kutty', 'owner_id': 1}]

```

## Documentation
Take a look at the [wiki here](https://github.com/byoso/silly_db/wiki#silly-db-wiki)