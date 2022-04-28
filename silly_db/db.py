import sqlite3
from silly_db.helpers import color


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

    def __iter__(self):
        return iter(self.items)

    def __add__(self, other):
        array = list(set([*self.items, *other.items]))
        return Selection(*array)

    def jsonify(self):
        """Returns an array of SelectionItems turned into dicts"""
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
    """Central object interacting with the database itself.
    params:
        - file (required): path to your desired [name].sqlite3 file
        - debug: default is True, shows or not some warnings.
    """
    def __init__(self, file: str = None, debug: bool = True):
        if file is None:
            raise ValueError(
                "Missing parameter for DB: file=some_file_name.sqlite3")
        self.debug = debug
        self.file = file
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def _read_sql_file(self, file: str) -> str:
        """Returns the content of a given file"""
        with open(file, 'r') as sql_file:
            commands = sql_file.read()
        return commands

    def _get_headers(self, cursor_description):
        """Gathers the headers from a query. In case of duplicated headers,
        renames them, and sends a warning (if self.debug is True)"""
        headers = [description[0] for description in cursor_description]
        uniques = []
        warning = False  # inform the user if the headers have been changed
        for header in headers:
            counter = 1
            if header not in uniques:
                uniques.append(header)
            else:
                uniques.append(header + f"_{counter}")
                counter += 1
                warning = True
        if warning and self.debug:
            print(
                color["warning"] +
                "\n!!! WARNING : ambiguous query :\n"
                "Headers with same names, silly_db arbitrarily "
                "changed some of your headers. Use '[name] as [other_name)]'"
                " in your SQL query to fix this.\n" +
                color['end']
                )
        return uniques

    def execute(self, command):
        """'Begin transaction' and 'commit' are automatically added
        to the command, so don't use this key words."""
        commands = command.strip().split(";")
        try:
            self.cursor.execute("BEGIN TRANSACTION;")
            for command in commands:
                self.cursor.execute(command)
            self.cursor.execute("COMMIT;")
        except sqlite3.OperationalError as e:
            print("sqlite3.OperationalError :")
            print(e)

    def migrate(self, file=None):
        """Execute the migrations from a .sql file"""
        if file is None:
            self.execute(
                "CREATE table 'dfoixzjk' (t INT); DROP TABLE 'dfoixzjk';")
        commands = self._read_sql_file(file)
        commands = commands.strip().split(";")
        try:
            for command in commands:
                self.cursor.execute(command)
        except sqlite3.OperationalError as e:
            print("sqlite3.OperationalError :")
            print(e)

    def export(self, file=None):
        """Exports the entire database to a given file,
         into a sql format."""
        if file is None:
            file = "backup_" + self.file + ".sql"
        with open(file, 'w') as f:
            for line in self.connection.iterdump():
                f.write(f"{line}\n")

    def export_structure(self, file=None):
        """Exports only the structure of the database to a given file,
        into a sql format."""
        if file is None:
            file = "structure_" + self.file + ".sql"
        self.cursor.execute("SELECT sql FROM sqlite_master;")
        with open(file, 'w') as f:
            f.write("BEGIN TRANSACTION;\n")
            for line in self.cursor.fetchall():
                f.write(f"{line[0]};\n")
            f.write("COMMIT;")

    def select(self, command: str) -> Selection:
        """Query tool, the parameter is a purely SQL query, but without
        the word SELECT at the beginig (as it's already the method name)
        """
        self.cursor.execute("SELECT " + command)
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
