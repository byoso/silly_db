
def text(text) -> str:
    """Cleans the string to be insertable into sql.
    fix the quote problem.
    """
    output = text.replace("'", "''")
    return output
