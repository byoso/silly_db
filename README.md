![logo silly db](https://i.goopics.net/60cef4.png)

# Silly DB


## It is ...
**Not an ORM**. Silly DB is a tool to quikly handle a sqlite3 database with python3.  DB.select() returns a Selection object, wich is convenient to manipulate.

Some SQL knowledge **is required**, the purpose of Silly DB is not to get rid of SQL (actualy, SQL is the best tool to manage... a SQL database), but to give a few helpers to make life easyer.

The required knowledge and much more is available here :

- https://www.sqlite.org/index.html
- https://docs.python.org/3/library/sqlite3.html#

You should consider using 'DB Browser for SQLite':

- https://sqlitebrowser.org/

No need to be an expert, just understand own to create a DB and use 'SELECT' will be fine (see the examples files to get quickly some bases).

## Fast way to begin

Create a new directory and open a console in there.
get a basic working structure:
```
$ python3 -m silly_db.plop db
```
execute the migrator:
```
$ ./migrator.py
```
Congratulations ! You got a database !
To understand how it works, open the differents files provided and read the comments, it will be easy to adapt to your own needs.

get more info with:
```
$ python3 -m silly_db
```
and more about the plop options here:
```
$ python3 _n silly_db.plop
```


## Silly DB gives a hand with:

- DB object (methods: execute, migrate, export, export_structure, select)
- Selection / SelectionItem
- Selection.exists() -> bool
- Selection.jsonify() -> list of dict
- Selection.\_\_add__() (new = selection1 + selection2 #without duplications)
- Selection.order_by(key='a_column_name', reverse=False)
- SelectionItem are convertible to dict: dico = dict(SelectionItem)

to start with a basic structure:
- plop

fix the sql 'quotes' problem with silly_db.helpers.text:
```python
name = text("tim's") # convert ' into '' (escaped quote)
db.execute(f"INSERT INTO 'guys' ('name') VALUES('{name}')")

```

## About queries
Queries are done just as it is in SQL, but with the DB.select() method. A query returns a Selection object (list of SelectionItem objects).
Attributes are automaticaly gathered from the query.

A Selection object can be converted into a json format.
```python
>>> some_json = selection.jsonify()
```

A SelectionItem object can be converted into a dict:
```python
>>> dico = dict(selection_item)
```
Short example:

```python
>>> selection = db.select(
    "cat.name as cat, person.name as owner FROM cat JOIN person ON "
    "cat.owner_id=person.id WHERE cat.owner_id=1"
    )
>>> print(selection)
<Selection[{cat: Chat, owner: Irina, }, {cat: snow_ball, owner: Irina, }, ]>
>>> selection.items[1].cat
'snow_ball'

```
