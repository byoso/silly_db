import os
import stat


def set_executable(file) -> None:
    st = os.stat(file)
    os.chmod(file, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def to_sql(value):
    """Cleans the data to be insertable into sql.
    - str: Fixes the quote problem.
    - None: becomes NULL
    - other: keep it as it is.
    """
    if isinstance(value, type(None)):
        sql_value = 'NULL'
    if type(value) == str:
        sql_value = value.replace("'", "''")
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
