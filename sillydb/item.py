

class Item:
    """An item have system 2 attribute:
    - id
    - in_table
    And its other attributes
    """

    def __repr__(self):
        attrs_show = ""
        for attr in vars(self):
            attrs_show += f"{attr}: {getattr(self, attr)}, "
        return f"<{attrs_show[:-2]}>"
