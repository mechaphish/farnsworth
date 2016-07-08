#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from playhouse.postgres_ext import PostgresqlExtDatabase    # For JSONB type

"""Database connection configurations."""

master_db = PostgresqlExtDatabase( # pylint: disable=invalid-name
    os.environ['POSTGRES_DATABASE_NAME'],
    user=os.environ['POSTGRES_DATABASE_USER'],
    password=os.environ['POSTGRES_DATABASE_PASSWORD'],
    host=os.environ['POSTGRES_MASTER_SERVICE_HOST'],
    port=os.environ['POSTGRES_MASTER_SERVICE_PORT'],
    register_hstore=False,
    autocommit=True,
    autorollback=True,
)

if os.environ.get('POSTGRES_USE_SLAVES') is not None:
    slave_db = PostgresqlExtDatabase( # pylint: disable=invalid-name
        os.environ['POSTGRES_DATABASE_NAME'],
        user=os.environ['POSTGRES_DATABASE_USER'],
        password=os.environ['POSTGRES_DATABASE_PASSWORD'],
        host=os.environ['POSTGRES_SLAVE_SERVICE_HOST'],
        port=os.environ['POSTGRES_SLAVE_SERVICE_PORT'],
        register_hstore=False,
    )
else:
    slave_db = None              # pylint: disable=invalid-name

def connect_dbs():
    """Open connection to databases"""
    for database in (master_db, slave_db):
        if database is not None:
            database.connect()

def close_dbs():
    """Close connection to databases"""
    for database in (master_db, slave_db):
        if database is not None and not database.is_closed():
            database.close()
