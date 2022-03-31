#! /usr/bin/env python3
# coding: utf-8

from table import Table
from connexion import ConnectorSQLITE, ConnectorJSON


class DB:
    def __init__(
        self,
        file='db.json',
        *args
            ):
        self.tables = []
        for arg in args:
            self.tables.append(arg)
        if file.split('.')[1] == 'sqlite3':
            self.do = ConnectorSQLITE(file)
        elif file.split('.')[1]:
            self.do = ConnectorJSON(file)
        else:
            raise ValueError("File must end by '.sqlite3' or '.json'")

    def add_tables(self, tables_list):
        for table in tables_list:
            self.tables.append(table)

    def __repr__(self):
        attrs_show = ""
        for attr in vars(self):
            attrs_show += f"{attr}: {getattr(self, attr)}, "
        return f"<SillyDB {attrs_show}>"

    def load(self):
        pass

    def save(self):
        pass