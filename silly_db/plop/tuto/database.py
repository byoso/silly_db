#! /usr/bin/env python3
# coding: utf-8

"""This module is where the database is instantiated"""

from silly_db.db import DB
import os

# Sets the .sqlit3 file alongside this database.py file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db = DB(file=os.path.join(BASE_DIR, 'my_db.sqlite3'))
