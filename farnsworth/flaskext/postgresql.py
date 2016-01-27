#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask extension that provides easy PostgreSQL connector functionality.
"""

from __future__ import absolute_import

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

import psycopg2
import psycopg2.extras

from flask import _request_ctx_stack


class PostgreSQL(object):
    """Flask object that wraps requests to provide PostgreSQL functionality
    transparently.

    Note: POSTGRES_SERVICE_UNIX_SOCKET takes preference over TCP parameters.
          Set it to None to use POSTGRES_SERVICE_HOST and PORT.
    """

    def __init__(self, app=None):
        """Initialize the PostgreSQL request extension for the Flask app ``app``.

        :param app: Flask application (optional)
        """
        self.app = app
        if self.app is not None:
            self.app = app
            self.app.config.setdefault('POSTGRES_SERVICE_UNIX_SOCKET', None)
            self.app.config.setdefault('POSTGRES_SERVICE_HOST', None)
            self.app.config.setdefault('POSTGRES_SERVICE_PORT', 5432)
            self.app.config.setdefault('POSTGRES_DATABASE_USER', None)
            self.app.config.setdefault('POSTGRES_DATABASE_PASSWORD', None)
            self.app.config.setdefault('POSTGRES_DATABASE_NAME', None)
            self.app.teardown_request(self.teardown_request)
            self.app.before_request(self.before_request)

    def connect(self):
        """Connect to the PostgreSQL database specified in the Flask
        application's configuration file.

        :return: PostgreSQL database connector.
        """
        kwargs = {}
        if self.app.config['POSTGRES_SERVICE_UNIX_SOCKET']:
            kwargs['unix_socket'] = self.app.config['POSTGRES_SERVICE_UNIX_SOCKET']
        else:
            if self.app.config['POSTGRES_SERVICE_HOST']:
                kwargs['host'] = self.app.config['POSTGRES_SERVICE_HOST']
            if self.app.config['POSTGRES_SERVICE_PORT']:
                kwargs['port'] = self.app.config['POSTGRES_SERVICE_PORT']
        if self.app.config['POSTGRES_DATABASE_USER']:
            kwargs['user'] = self.app.config['POSTGRES_DATABASE_USER']
        if self.app.config['POSTGRES_DATABASE_PASSWORD']:
            kwargs['password'] = self.app.config['POSTGRES_DATABASE_PASSWORD']
        if self.app.config['POSTGRES_DATABASE_NAME']:
            kwargs['dbname'] = self.app.config['POSTGRES_DATABASE_NAME']
        return psycopg2.connect(**kwargs)    # pylint:disable=star-args

    def before_request(self):
        """Connect to the database before handling the request.
        """
        ctx = _request_ctx_stack.top
        ctx.database = self.connect()
        ctx.database.autocommit = True

    # pylint:disable=unused-argument,no-self-use
    def teardown_request(self, exception):
        """After handling the request, close the database connection.
        """
        ctx = _request_ctx_stack.top
        if hasattr(ctx, "cursor"):
            ctx.cursor.close()
        if hasattr(ctx, "database"):
            ctx.database.close()
    # pylint:enable=unused-argument,no-self-use

    @property
    def database(self):  # pylint:disable=no-self-use
        """Ugly, but convenient access to the existing database connection.

        :return: PostgreSQL database connector.
        """
        ctx = _request_ctx_stack.top
        if ctx is not None:
            return ctx.database

    def cursor(self, dictionary=True, **kwargs):  # pylint:disable=no-self-use
        """Create and return a cursor for the current database connection.

        :param bool dictionary: flag if the cursor should return rows as
                                dictionaries (optional, True by default).
        :param **kwargs: optional keyword arguments that are passed to the
                         cursor initalization function.
        :return: database cursor :)
        """
        ctx = _request_ctx_stack.top
        if ctx is not None:
            if dictionary:
                return ctx.database.cursor(cursor_factory=psycopg2.extras.RealDictCursor, **kwargs)
            else:
                return ctx.database.cursor(**kwargs)
