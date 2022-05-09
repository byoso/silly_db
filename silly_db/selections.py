"""Objects and tools used for the selections from the database.
- Selection
- SelectionItem
- Model
"""

from silly_db.exceptions import SillyDbError


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

    def jsonify(self):
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

    def fusion_in(self, attr_name, item, in_place_of=None):
        """Include another item into self as an attribute"""
        setattr(self, attr_name, item)
        if in_place_of is not None:
            self.remove(in_place_of)
        return self

    def fusion_on(self, item, in_place_of=None):
        """Fusion with another item"""
        if in_place_of is not None:
            self.remove(in_place_of)
        attrs = vars(item)
        for attr in attrs:
            setattr(self, attr, getattr(item, attr))
        return self

    def remove(self, *args):
        """remove one or more attributes"""
        for arg in args:
            delattr(self, arg)
        return self


class Model:
    """DB.model() instanciates a Model"""
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
