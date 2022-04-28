
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
