from sillydb.item import ModelItem
from sillydb.table import ModelTable


version = "1.0.0"


class ModelDB:
    def __init__(
        self, model_table=ModelTable, *args
            ):
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
