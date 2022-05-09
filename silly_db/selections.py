"""Objects and tools used for the selections from the database.
- Selection
- SelectionItem
- Model
"""

from silly_db.exceptions import SillyDbError
from silly_db.helpers import color, insert_to_sql


class Selection:
    """Object returned by the DB.select method, it contains the result
    of the query in a convenient form allowing easy manipulations.
    - self.items is a list of SelectionItems."""
    def __init__(self, *args):
        self.items = [*args]

    def __str__(self) -> str:
        display = "<Selection["
        for elem in self.items:
            display += str(elem)+", "
        display += "]>"
        return display

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __add__(self, other):
        array = list(set([*self.items, *other.items]))
        return Selection(*array)

    def jsonify(self) -> list:
        """Returns an array of SelectionItems turned into dicts"""
        array = []
        for item in self.items:
            array.append(dict(item))
        return array

    def exists(self) -> bool:
        if len(self.items) > 0:
            return True
        return False

    def order_by(self, key=None, reverse=False):
        return sorted(
            self.items, key=lambda x: getattr(x, key), reverse=reverse)


class SelectionItem:
    """db.select() will build SelectionItems with some given attributes
    and create a Selection object, filled with SelectionItems"""
    def __init__(self, dico=None, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if dico is not None:
            for key, value in dico.items():
                setattr(self, key, value)

    def __str__(self) -> str:
        return f"<SelItem{str(dict(self))}>"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        """dict(SelectionItem) converts the
        SelectionItem into a dict recursively"""
        for attr in vars(self):
            if isinstance(getattr(self, attr), SelectionItem):
                setattr(self, attr, dict(getattr(self, attr)))
            yield attr, getattr(self, attr)

    def _copy(self):
        new = SelectionItem()
        for attr in vars(self):
            setattr(new, attr, getattr(self, attr))
        return new

    def fusion_in(self, attr_name, item, in_place_of=None):
        """Include another item into self as an attribute"""
        copy = self._copy()
        setattr(copy, attr_name, item)
        if in_place_of is not None:
            copy.remove(in_place_of)
        return copy

    def fusion_on(self, item, in_place_of=None):
        """Fusion with another item"""
        copy = self._copy()
        if in_place_of is not None:
            copy.remove(in_place_of)
        attrs = vars(item)
        for attr in attrs:
            setattr(copy, attr, getattr(item, attr))
        return copy

    def remove(self, *args):
        """remove one or more attributes"""
        for arg in args:
            delattr(self, arg)
        return self

    def jsonify(self) -> dict:
        return dict(self)


class Model:
    """DB.model() instanciates a Model
    - db is provided automaticaly by db.model(), do not care
    - table is a str (the name of your SQL table)
    """
    def __init__(self, db, table):
        self._db = db
        self._table = table

    def all(self, columns="*"):
        "returns a Selection of all the rows in the table"
        selection = self._db.select(f"{columns} FROM {self._table}")
        return selection

    def filter(self, condition, columns="*"):
        """returns a Selection"""
        selection = self._db.select(
            f"{columns} FROM {self._table} WHERE {condition}"
            )
        return selection

    def get(self, condition, columns="*"):
        """returns a unique SelectionItem object, or an exception if
        multiple results, or None if no result"""
        selection = self.filter(condition, columns)
        if len(selection) > 1:
            raise SillyDbError(
                "Model.get returning multiple items. The condition "
                "must target only one result, you should use a unique id."
                )
        if not selection.exists():
            return None
        else:
            return selection[0]

    def get_id(self, id, columns="*"):
        """Shortcut to self.get("id=...")"""
        return self.get(f"id={id}", columns)

    def insert(self, **kwargs):
        if len(kwargs) == 0 and self._db.debug:
            message = (
                color['warning'] + "Warning : Empty insert in model" +
                color['end']
                )
            print(message)
        keys = ""
        values = ""
        for key in kwargs:
            keys += key + ", "
            value = insert_to_sql(kwargs[key])
            values += f"{value}, "
        keys = keys[:-2]
        values = values[:-2]
        command = (
            f"INSERT OR REPLACE INTO {self._table} ({keys}) VALUES ({values})"
            )
        self._db.execute(command)

    def delete(self, condition=None):
        if condition is not None:
            command = f"DELETE FROM {self._table} WHERE {condition}"
            self._db.execute(command)

    def update(self, condition=None, **kwargs):
        command = f"UPDATE {self._table} SET "
        values = ""
        for key in kwargs:
            values += f"{key}={insert_to_sql(kwargs[key])}, "
        values = values[:-2]
        command += values + " WHERE " + condition
        self._db.execute(command)


class VirtualModel:
    """
    VirtualModel(db, *args)

    - db is automatically provided by db.view(), do not care.

    args must be organized like that:
    - <tuple>, <jointure(str)>, <tuple>...
    - tuple: ( table(str), columns(str) )
        if columns is "*", all the colums will be present, but renamed
        into : "table" + "_" + "column_name"
    - jointure: corresponds to the 'ON' key word in SQL.
        ex: "cat.owner_id=person.id"
    """
    def __init__(self, db, *args):
        if (len(args) - 1) % 2 != 0:
            raise SillyDbError("Unexpected args number in VirtualView")
        self._db = db
        self.tables = []
        self.db_params = {}
        self.jointures = []
        for arg in args:
            if args.index(arg) % 2 == 0:
                self._tuple_treatment(arg)
            else:
                self.jointures.append(arg)
        # print(self.db_params)
        # print(self.jointures)

    def _tuple_treatment(self, arg):
        """Sort the given args into self.db_params and self.jointures"""
        table = arg[0]
        self.tables.append(table)
        if "*" in arg[1]:
            reals = self._db.query(f"PRAGMA table_info ({table});")
            for real in reals:
                name = table + "_" + real.name
                self.db_params[name] = (table, real.name)
        else:
            columns = arg[1].split(",")
            for column in columns:
                if "as" not in column.lower():
                    self.db_params[column] = (table, column.strip())
                else:
                    array = column.lower().split("as")
                    real = array[0]
                    alias = array[1]
                    if alias in self.db_params:
                        raise SillyDbError(
                            "Columns name duplication in VirtualModel, use"
                            "aliases to fix this"
                            )
                    self.db_params[alias] = (table, real)

    def _get_columns(self, columns):
        """return the composed part of the command
        'column AS alias, ...'"""
        tables_to_get = ""
        columns_to_get = ""
        if columns != "*":
            columns = columns.split(",")
            for column in columns:
                column.strip()
                columns_to_get += (
                    self.db_params[column][0] +
                    "."+self.db_params[column][1] +
                    " AS " + column + ", "
                )
                tables_to_get += self.db_params[column][0]
        else:
            for column in self.db_params:
                columns_to_get += (
                    self.db_params[column][0] +
                    "."+self.db_params[column][1] +
                    " AS " + column + ", "
                )
                tables_to_get += self.db_params[column][0]
        return columns_to_get[:-2]

    def _get_tables_joins(self):
        """return the composed part of the command
        'table JOIN table ON <condition>"""
        joins = self.tables[0]
        for join in self.jointures:
            index = self.jointures.index(join)
            joins += " JOIN " + self.tables[index+1]
            joins += " ON " + join

        return joins

    def all(self):
        """VirtualModel does not support aliases in queries, you have to
        define it when the VirtualModel is created if you whant some."""
        command = "SELECT "
        columns = self._get_columns("*")
        command += columns + " FROM " + self._get_tables_joins()
        selection = self._db.query(command)
        return selection

    def filter(self, condition):
        """returns a Selection"""
        command = "SELECT "
        columns = self._get_columns("*")
        command += columns + " FROM " + self._get_tables_joins()
        command += " WHERE " + condition
        selection = self._db.query(command)
        return selection
