import os
import stat


def set_executable(file) -> None:
    st = os.stat(file)
    os.chmod(file, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def text(text: str) -> str:
    """Cleans the string to be insertable into sql.
    Fixes the quote problem.
    """
    output = text.replace("'", "''")
    return output


# color parameters: style;background (30 is none);foreground
color = {
    "end": "\x1b[0m",
    "warning": "\x1b[0;30;33m"
}
