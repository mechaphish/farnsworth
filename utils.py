#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A collection of utilities to make developing easier :)
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"

from flask import Response

import datetime
import functools
import json


def _json_serialize(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, buffer):
        return str(obj)


def jsonify(func):
    """Decorator to jsonify return values of functions.

    :param function func: Function wrapped to return JSON instead of Python objects.
    """
    @functools.wraps(func)
    def wrapper(**kwds):     # pylint: disable=missing-docstring
        return Response(json.dumps(func(**kwds), default=_json_serialize),
                        mimetype='application/json')
    return wrapper


def filter_query(query, filters, arguments):
    _filters = {}
    for f in filters:
        _filters["{} = %s".format(f)] = arguments.get(f)

    # We cannot use a dict comprehension here with keys() and values() after
    # because their order is not guaranteed to be the same.
    filter_stmts, filter_values = [], []
    for stmt, value in _filters.items():
        if value is not None:
            filter_stmts.append(stmt)
            filter_values.append(value)
    filter_stmt = " AND ".join(filter_stmts)
    filter_values = tuple(filter_values)

    if filter_stmt:
        return "{} WHERE {}".format(query, filter_stmt), filter_values
    else:
        return query, []


def update_query(table, updates, where):
    # We need to build the updates statement
    _updates = {}
    for k, v in updates.items():
        _updates["{} = %s".format(k)] = v
    _updates["updated_at = %s"] = datetime.datetime.now()

    # We cannot use a dict comprehension here with keys() and values() after
    # because their order is not guaranteed to be the same.
    update_stmts, update_values = [], []
    for stmt, value in _updates.items():
        if value is not None:
            update_stmts.append(stmt)
            update_values.append(value)
    update_stmt = ", ".join(update_stmts)

    # We have to do the same for the where clause
    _where = {}
    for k, v in where.items():
        _where["{} = %s".format(k)] = v

    # We cannot use a dict comprehension here with keys() and values() after
    # because their order is not guaranteed to be the same.
    where_stmts, where_values = [], []
    for stmt, value in _where.items():
        if value is not None:
            where_stmts.append(stmt)
            where_values.append(value)
    where_stmt = " AND ".join(where_stmts)

    # Return the created query
    update_query = "UPDATE {} SET {} WHERE {}"

    if update_stmt:
        return update_query.format(table, update_stmt, where_stmt), \
            tuple(update_values + where_values)
    else:
        return "", []
