#! /usr/bin/env python3
# coding: utf-8


class Field:
    """A Field have 3 attirbutes:
    - name
    - type
    - value
    """
    number = 0

    def __init__(self, name="", type=str, value=None):
        if name == "":
            self.name = f"noname {self.number}"
            self.number += 1
        self.name = name
        self.type = type
        # user can set a default value when defining the Field
        if value is None:
            self.value = self.type()
        else:
            try:
                self.type(self.value)
            except ValueError:
                raise ValueError(
                    "Field created with default value not maching type")
            self.value = value

    def get(self):
        return self.value
