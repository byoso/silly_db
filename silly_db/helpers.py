import os
import stat
import hashlib


def hasher(file):
    """Returns the sha1 hash of a file"""
    BLOCK_SIZE = 65536
    hash = hashlib.sha1()
    with open(file, 'r') as f:
        fb = f.read(BLOCK_SIZE).encode('utf-8')
        while len(fb) > 0:
            hash.update(fb)
            fb = f.read(BLOCK_SIZE).encode('utf-8')
    return hash.hexdigest()


def set_executable(file) -> None:
    """set a file executable, used within plop"""
    st = os.stat(file)
    os.chmod(file, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def insert_to_sql(value):
    """Cleans the input data to be insertable into sql.
    - str: Fixes the quote problem.
    - None: becomes NULL
    - other: keep it as it is.
    """

    if isinstance(value, type(None)):
        sql_value = 'NULL'
    elif type(value) == str:
        sql_value = value.replace(
                    "'", "''")
        sql_value = f"'{sql_value}'"
    else:
        sql_value = value
    return sql_value


# color parameters: style;background (30 is none);foreground
color = {
    "end": "\x1b[0m",
    "info": "\x1b[0;30;36m",
    "success": "\x1b[0;30;32m",
    "warning": "\x1b[0;30;33m",
    "danger": "\x1b[0;30;31m",
}


INITIALIZE_DB = """
CREATE TABLE IF NOT EXISTS "_migrations_applied" (
    "id" INTEGER NOT NULL,
    "file" TEXT NOT NULL,
    "date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "sha1" TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
);

"""
