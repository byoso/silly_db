import os
import sqlite3


class Selection:
    def __init__(self, *args):
        self.items = [*args]

    def __str__(self) -> str:
        display = "<Selection["
        for elem in self.items:
            display += str(elem)+", "
        display += "]>"
        return display

    def __iter__(self):
        return iter(self.items)

    def __add__(self, other):
        array = list(set([*self.items, *other.items]))
        return Selection(*array)

    def jsonify(self):
        """returns an array of dicts"""
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
        return str(dict(self))

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        """dict(SelectionItem) converts the
        SelectionItem into a dict"""
        for attr in vars(self):
            yield attr, getattr(self, attr)


class DB:
    def __init__(self, file=None):
        if file is None:
            raise ValueError(
                "Missing parameter for DB: file=some_file_name.sqlite3")
        self.file = file
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

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

    def migrate(self, file=None):
        """Execute the migrations from a .sql file"""
        if file is None:
            self.execute(
                "CREATE table 'dfoixzjk' (t INT); DROP TABLE 'dfoixzjk';")
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
