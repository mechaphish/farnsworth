#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from playhouse.pool import PooledPostgresqlExtDatabase  # For JSONB type
from playhouse.shortcuts import RetryOperationalError
from retrying import retry

"""Database connection configurations."""

class RetryHarderOperationalError(object):
    def execute_sql(self, sql, params=None, require_commit=True):
        @retry(wait_exponential_mulitplier=500,
               wait_exponential_max=10000,
               stop_max_attempt_number=10)
        def execute():
            try:
                cursor = super(RetryOperationalError, self).execute_sql(
                    sql, params, require_commit)
            except OperationalError:
                if not self.is_closed():
                    self.close()
                with self.exception_wrapper():
                    cursor = self.get_cursor()
                    cursor.execute(sql, params or ())
                    if require_commit and self.get_autocommit():
                        self.commit()
            return cursor
        return execute()


class RetryPooledPostgresqlExtDatabase(PooledPostgresqlExtDatabase,
                                       RetryHarderOperationalError):
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
    max_connections=os.environ.get('POSTGRES_MASTER_CONNECTIONS', 2),
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
        max_connections=os.environ.get('POSTGRES_SLAVE_CONNECTIONS', 2),
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
