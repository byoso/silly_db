# Silly DB
### *Still a WIP...*
Done:
- DB (methods: execute, migrate, export, export_structure, select)
- Selection / SelectionItem

Todo next:
- Selection.jsonify()
- Selection.exists()
- Selection.add()



## It is ...
**Not an ORM**. Silly DB is a tool to quikly handle a sqlite3 database with python3.  DB.select() returns a Selection object, wich is convenient to manipulate.

Some SQL knowledge **is required**, the purpose of Silly DB is not to get rid of SQL (actualy, SQL is the best tool to manage... a SQL database), but to give a few helpers to make life easyer.

The required knowledge and much more is available here :

- https://www.sqlite.org/index.html
- https://docs.python.org/3/library/sqlite3.html#

You should consider using 'DB Browser for SQLite':

- https://sqlitebrowser.org/

No need to be an expert, just understand own to create a DB and use 'SELECT' will be fine (see the examples files to get quickly some bases).

## examples

Create a database:
```python
from silly_db.db import DB

db = DB('my_db.sqlite3', initial_sql="initial.sql")
```

Query example:
```python
>>>selection = db.select(
    "cat.name as cat, person.name as owner FROM cat JOIN person ON "
    "cat.owner_id=person.id WHERE cat.owner_id=1")
>>> print(selection)
<Selection[{cat: Chat, owner: Irina, }, {cat: snow_ball, owner: Irina, }, ]>
>>> selection.items[1].cat
'snow_ball'

```
