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

from database import db


db.migrate('migrations/initial.sql')
db.migrate('migrations/populate.sql')
