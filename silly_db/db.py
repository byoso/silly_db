import os
import sqlite3


class Selection:
    def __init__(self, *args):
        self.items = [*args]

    def __str__(self):
        display = "<Selection["
        for elem in self.items:
            display += str(elem)+", "
        display += "]>"
        return display

    @property
    def json(self):
        array = []
        for elem in self.items:
            array.append(elem.json)
        return array


class SelectionItem:
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
            try:
                self.cursor.execute(command)
            except sqlite3.OperationalError as e:
                print("sqlite3.OperationalError")
                print(command)
                print(e)

    def migrate(self, file):
        """Execute the migrations from a .sql file"""
        commands = self._read_sql_file(file)
        self.execute(commands)

    def export(self, file=None):
        if file is None:
            file = "backup_" + self.file + ".sql"
        with open(file, 'w') as f:
            for line in self.connection.iterdump():
                f.write(f"{line}\n")

    def export_structure(self, file=None):
        if file is None:
            file = "structure_" + self.file + ".sql"
        self.cursor.execute("SELECT sql FROM sqlite_master;")
        with open(file, 'w') as f:
            f.write("BEGIN TRANSACTION;\n")
            for line in self.cursor.fetchall():
                f.write(f"{line[0]};\n")
            f.write("COMMIT;")

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
            response = SelectionItem()
            for key in dico:
                setattr(response, key, dico[key])
            responses.append(response)
        query_set = Selection(*responses)
        return query_set
