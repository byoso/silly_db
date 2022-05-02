#! /usr/bin/env python3
# coding: utf-8


from silly_db.db import DB
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


db = DB(file=os.path.join(BASE_DIR, 'my_db.sqlite3'))
