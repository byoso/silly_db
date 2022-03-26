

class ModelItem:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs_show = ""
        for attr in self.__dict__:
            attrs_show += f"{attr}: {getattr(self, attr)}, "
        return f"<{attrs_show[:-2]}>"
