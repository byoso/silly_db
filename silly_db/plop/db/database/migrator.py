#! /usr/bin/env python3
# coding: utf-8

"""Execute this file to apply your migrations.

A migration file (some_file_name.sql) must always contain:

BEGIN TRANSACTION;
[...your migrations...]
COMMIT;

If you want to pre-populate your DB, do it in a dedicated file.

Once the migrations are done, comment the lines to be sure not to migrate
twice the same thing, but keep your migrations at hand if you need to
rebuild your db.

"""

import os
from database import db

migdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'migrations')


db.migrate(migdir + '/initial.sql')
db.migrate(migdir + '/populate.sql')
