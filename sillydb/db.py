

version = "1.0.0"


class ModelItem:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs_show = ""
        for attr in self.__dict__:
            attrs_show += f"{attr}: {getattr(self, attr)}, "
        return f"<{attrs_show}>"

    def __str__(self):
        attrs_show = ""
        for attr in self.__dict__:
            attrs_show += f"{attr:>10}: {getattr(self, attr):<10} "
        return attrs_show


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
        return self.items

    def filter(self, key, value):
        items_filtered = filter(lambda x: getattr(x, key) == value, self.items)
        return list(items_filtered)

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
            attrs_show += f"{attr}: {getattr(self, attr)}, "
        return f"<{attrs_show}>"


class ModelDB:
    def __init__(
        self, model_item=ModelItem, model_table=ModelTable, *args
        ):
        self.model_item = model_item
        self.model_table = model_table
        self.tables = []
        for arg in args:
            self.tables.append(arg)

    def add_tables(self, tables_list):
        for table in tables_list:
            self.tables.append(table)

    def __repr__(self):
        attrs_show = ""
        for attr in self.__dict__:
            attrs_show += f"{attr}: {getattr(self, attr)}, "
        return f"<SillyDB {attrs_show}>"


class Selection:
    def __init__(self):
        self.content = []
