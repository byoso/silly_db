#! /usr/bin/env python3
# coding: utf-8

import os
import sqlite3


class Queryset:
    def __init__(self, *args):
        self.objects = [*args]

    def __str__(self):
        display = "<Queryset["
        for elem in self.objects:
            display += str(elem)+", "
        display += "]>"
        return display

    @property
    def json(self):
        array = []
        for elem in self.objects:
            array.append(elem.json)
        return array


class Response:
    def __str__(self) -> str:
        display = "{"
        attrs = vars(self)
        for attr in attrs:
            display += f"{attr}: {getattr(self, attr)}, "
        display += "}"
        return display

    def __repr__(self):
        return str(self)

    @property
    def json(self):
        json = str(self)
        return json


class DB:
    def __init__(self, file=None, initial_sql=None):
        if initial_sql is not None:
            if os.path.exists(os.path.abspath(file)):
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
            else:
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
                commands = self._read_sql_file(initial_sql)
                self.execute(commands)
        if initial_sql is None:
            if os.path.exists(os.path.abspath(file)):
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
            else:
                self.connection = sqlite3.connect(file)
                self.cursor = self.connection.cursor()
                self.execute("CREATE table 'a' (t INT); DROP TABLE 'a';")
        self.file = file

    def _read_sql_file(self, file):
        with open(file, 'r') as sql_file:
            commands = sql_file.read()
        return commands

    def _get_headers(self, cursor_description):
        headers = [description[0] for description in cursor_description]
        uniques = []
        for header in headers:
            counter = 1
            if header not in uniques:
                uniques.append(header)
            else:
                uniques.append(header + f"_{counter}")
                counter += 1
        return uniques

    def execute(self, command):
        commands = command.strip().split(";")
        for command in commands:
            self.cursor.execute(command)

    def migrations(self, file):
        """Execute the migrations from a .sql file"""
        commands = self._read_sql_file(file)
        self.execute(commands)

    def select(self, command):
        self.execute("SELECT " + command)
        headers = self._get_headers(self.cursor.description)
        results = self.cursor.fetchall()
        answers = []
        responses = []
        for result in results:
            elem = dict(zip(headers, result))
            answers.append(elem)
        for answer in answers:
            dico = dict(answer.items())
            response = Response()
            for key in dico:
                setattr(response, key, dico[key])
            responses.append(response)
        query_set = Queryset(*responses)
        return query_set


db = DB('my_db.sqlite3', initial_sql="initial.sql")
query = db.select(
    "* FROM cat JOIN person ON cat.owner_id=person.id WHERE cat.owner_id=1")

print(query.json)
print(query.objects[0].name)

cat = db.select("* from cat where id=2").objects[0]
print(cat.name)
print(cat.owner_id)


query2 = db.select(
    "cat.name as cat, person.name as owner FROM cat JOIN person ON cat.owner_id=person.id WHERE cat.owner_id=1")
print(query2)
print(query2.objects[0].cat)
print(query2.objects[1].cat)
