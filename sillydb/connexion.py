#! /usr/bin/env python3
# coding: utf-8

import sqlite3


class ConnectorSQLITE:
    def __init__(self, file):
        self.file = file
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()


class ConnectorJSON:
    pass