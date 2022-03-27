from sillydb.item import Item
from sillydb.selection import Selection
from sillydb.fields import Field
from sillydb.helpers import EmptyClass


class ModelTable:

    def __init__(
        self, base_id=1, fields=[],
            model_field=Field):
        self.model_field = model_field
        self.fields = fields
        self.base_id = base_id
        self.items = []

    def create(self, *args, **kwargs):
        """Item creation in the DB"""
        item = Item()
        item.id = self.base_id
        self.base_id += 1
        # fill the fields while checking if the entry is the good type.
        # empty fields are filled with the entry type value (ex: str())
        for field in self.fields:
            index = self.fields.index(field)
            if len(args) > index:
                if isinstance(args[index], self.fields[index].type):
                    setattr(item, self.fields[index].name, args[index])
                else:
                    raise ValueError(
                        f"Item creation: {args[index]} "
                        f"is not {self.fields[index].type}")
            else:
                setattr(
                    item, self.fields[index].name,
                    self.fields[index].type()
                )
        for key, value in kwargs.items():
            field = list(filter(lambda x: x.name == key, self.fields))[0]
            if isinstance(value, field.type):
                setattr(item, key, value)
            else:
                raise ValueError(
                    f"Item creation: {args[index]} "
                    f"is not {self.fields[index].type}")

        self.items.append(item)

    def all(self):
        return Selection(self.items)

    def update_all(self, **kwargs):
        for item in self.all():
            for key, value in kwargs.items():
                setattr(item, key, value)

    def update(self, id, **kwargs):
        pass

    def delete(self, id):
        self.items.remove(self.get(id=id))

    def get(self, **kwargs):  # TODO : get it better
        items_filtered = self.all()
        for key, value in kwargs.items():
            if key == "id":
                items_filtered = list(filter(lambda x: x.id == value, self.items))
                return items_filtered[0]
            else:
                items_filtered = list(filter(lambda x: getattr(x, key) == value, items_filtered))
            return items_filtered

    def __repr__(self):
        attrs_show = ""
        for attr in vars(self):
            if attr != 'items':
                attrs_show += f"{attr}: {getattr(self, attr)}, "
        attrs_show += f"items: {len(self.items)}"
        return f"<{attrs_show}>"
