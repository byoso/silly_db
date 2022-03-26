
class Selection:
    def __init__(self, *args):
        self.content = set(*args)

    def __repr__(self):
        display = f"\n<Selection items:{len(self.content)}"
        for item in self.content:
            display += f"\n- {item}"
        display += "\n>"
        return display

    def filter_lambda(self, func):
        result = filter(func, self.content)
        return Selection(result)

    def id_get(self, id):
        items = list(filter(lambda x: x.id == id, self.content))
        if len(items) > 0:
            return items[0]

    def __add__(self, other):
        result = self.content | other.content
        return Selection(result)

    def __sub__(self, other):
        result = self.content - other.content
        return Selection(result)

    def __or__(self, other):
        self.__add__(self, other)

    def __and__(self, other):
        result = self.content & other.content
        return Selection(result)

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        return iter(self.content)

    def sort_by(self, attribute):
        if attribute.startswith('-'):
            result = sorted(self.content, key=lambda x: getattr(
                x, attribute[1:]), reverse=True)
        else:
            result = sorted(self.content, key=lambda x: getattr(
                x, attribute), reverse=False)
        return result
