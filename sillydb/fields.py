
class ModelField:
    number = 0

    def __init__(self, name="", type=str()):
        if name == "":
            self.name = f"noname {self.number}"
            self.number += 1
        self.name = name
        self.type = type
