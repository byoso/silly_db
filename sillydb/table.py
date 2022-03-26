from sillydb.item import ModelItem
from sillydb.selection import Selection





class ModelTable:

    def __init__(self, base_id=1, fields=[], model_item=ModelItem):
        self.model_item = ModelItem
        self.fields = fields
        self.base_id = base_id
        self.items = []

    def create(self, *args, **kwargs):
        item = self.model_item()
        item.id = self.base_id
        self.base_id += 1
        for field in self.fields:
            index = self.fields.index(field)
            if len(args) > index:
                setattr(item, self.fields[index], args[index])
            else:
                setattr(item, self.fields[index], None)
        for key, value in kwargs.items():
            setattr(item, key, value)
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
        self.items.remove(self.get(id))

    def get(self, id):
        items_filtered = list(filter(lambda x: x.id == id, self.items))
        if len(items_filtered) > 0 and len(items_filtered) < 2:
            return items_filtered[0]

    def __repr__(self):
        attrs_show = ""
        for attr in self.__dict__:
            if attr != 'items':
                attrs_show += f"{attr}: {getattr(self, attr)}, "
        attrs_show += f"items: {len(self.items)}"
        return f"<{attrs_show}>"
