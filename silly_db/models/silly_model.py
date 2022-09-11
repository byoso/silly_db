from silly_db.exceptions import SillyDbError
from silly_db.helpers import color, insert_to_sql


class Silly:
    """Actions on the model should be only there, not in the model directly."""
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
        if id is None:
            return None
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

        self._db.cursor.execute("BEGIN TRANSACTION;")
        self._db.cursor.execute(command)
        self._db.cursor.execute("COMMIT;")

    def delete(self, condition=None):
        if condition is not None:
            command = f"DELETE FROM {self._table} WHERE {condition}"
            self._db.cursor.execute("BEGIN TRANSACTION;")
            self._db.cursor.execute(command)
            self._db.cursor.execute("COMMIT;")

    def update(self, condition=None, **kwargs):
        command = f"UPDATE {self._table} SET "
        values = ""
        for key in kwargs:
            values += f"{key}={insert_to_sql(kwargs[key])}, "
        values = values[:-2]
        command += values + " WHERE " + condition
        self._db.cursor.execute("BEGIN TRANSACTION;")
        self._db.cursor.execute(command)
        self._db.cursor.execute("COMMIT;")


class SillyModel:
    """DB.model() instanciates a SillyModel
    parameters:
    - db is provided automaticaly by db.model(), do not care
    - table is a str (the name of your SQL table)

    The actions are exectued throught a Silly object, while the datas
    are actualy stocked in the SillyModel
    """
    def __init__(self, db, table):
        self.sil = Silly(db, table)
