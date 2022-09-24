"""Objects and tools used for the selections from the database.
- Selection
- SelectionItem
- Model
"""

import json


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
        if isinstance(other, SelectionItem):
            self.items.append(other)
            return self
        array = [*self, *other]
        return Selection(*array)

    def jsonify(self) -> list:
        """Returns an array of SelectionItems turned into dicts"""
        array = []
        for item in self.items:
            if isinstance(item, SelectionItem):
                array.append(dict(item))
            else:
                array.append(item.jsonify())
        return json.dumps(array)

    def exists(self) -> bool:
        if len(self.items) > 0:
            return True
        return False

    def order_by(self, key=None, reverse=False, case=False):
        if case:
            return Selection(*sorted(
                self.items, key=lambda x: getattr(x, key), reverse=reverse))
        else:
            return Selection(*sorted(
                self.items, key=lambda x: getattr(
                    x, key).upper(), reverse=reverse))

    def filter(self, func):
        return Selection(*filter(func, self.items))


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
            object = getattr(self, attr)
            if isinstance(object, SelectionItem):
                object = dict(object)
            if isinstance(object, Selection):
                object = object.jsonify()
            yield attr, object

    def __add__(self, other):
        selection = Selection() + self + other
        return selection

    def _copy(self):
        new = SelectionItem()
        for attr in vars(self):
            setattr(new, attr, getattr(self, attr))
        return new

    def remove(self, *args):
        """remove one or more attributes"""
        for arg in args:
            delattr(self, arg)
        return self

    def jsonify(self) -> dict:
        return json.dumps(dict(self))
