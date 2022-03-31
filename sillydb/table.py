#! /usr/bin/env python3
# coding: utf-8


from field import Field


class Table:

    def __init__(
        self, base_id=1, fields=[],
            model_field=Field):
        self._items = {}  # {id: {key: value, key, value...}}
        self.fields = {}  # {name: field, name: field}
        self.base_id = base_id

    def create(**kwargs):
        pass

    @property
    def items(self):
        # actions: get,
        pass

    def get():
        pass
