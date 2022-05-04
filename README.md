![logo silly db](https://i.goopics.net/60cef4.png)

# Silly DB


## It is ...
**Not an ORM**, even though it may "look and feel like" one in some aspects.

- Build the structure of your DB from classic .sql files.
- Queries return directly usefull python objects like an ORM would do.

Some SQL knowledge **is required**, the purpose of Silly DB is not to get rid of SQL (actualy, SQL is the best tool to manage... a SQL database), but to handle the boring things, and let you focus on your application.

The required knowledge and much more is available here :

- https://www.sqlite.org/index.html

You should consider using 'DB Browser for SQLite':

- https://sqlitebrowser.org/

No need to be an expert, just understand own to create a DB and use 'SELECT' will be fine (see the examples files to get quickly some bases).

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


## Silly DB gives a hand with:

- DB object (methods: execute, migrate, export, export_structure, select)
- Selection / SelectionItem
- Selection.exists() -> bool
- Selection.jsonify() -> list of dict
- Selection.\_\_add__() (new = selection1 + selection2 #without duplications)
- Selection.order_by(key='a_column_name', reverse=False)
- SelectionItem are convertible to dict: dico = dict(SelectionItem)
- Migrations made easy

- Quick start with plop

And some more...
fix the sql 'quotes' problem with silly_db.helpers.to_sql:
```python
name = to_sql("tim's") # convert ' into '' (escaped quote)
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
