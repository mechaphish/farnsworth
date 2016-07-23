#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from playhouse.pool import PooledPostgresqlExtDatabase  # For JSONB type
from playhouse.shortcuts import RetryOperationalError

"""Database connection configurations."""


class RetryPooledPostgresqlExtDatabase(PooledPostgresqlExtDatabase, RetryOperationalError):
    pass


master_db = RetryPooledPostgresqlExtDatabase(   # pylint: disable=invalid-name
    os.environ['POSTGRES_DATABASE_NAME'],
    user=os.environ['POSTGRES_DATABASE_USER'],
    password=os.environ['POSTGRES_DATABASE_PASSWORD'],
    host=os.environ['POSTGRES_MASTER_SERVICE_HOST'],
    port=os.environ['POSTGRES_MASTER_SERVICE_PORT'],
    register_hstore=False,
    autocommit=True,
    autorollback=True,
    max_connections=20,
    stale_timeout=60
)


if os.environ.get('POSTGRES_USE_SLAVES') is not None:
    slave_db = RetryPooledPostgresqlExtDatabase(    # pylint: disable=invalid-name
        os.environ['POSTGRES_DATABASE_NAME'],
        user=os.environ['POSTGRES_DATABASE_USER'],
        password=os.environ['POSTGRES_DATABASE_PASSWORD'],
        host=os.environ['POSTGRES_SLAVE_SERVICE_HOST'],
        port=os.environ['POSTGRES_SLAVE_SERVICE_PORT'],
        register_hstore=False,
        max_connections=40,
        stale_timeout=60
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
