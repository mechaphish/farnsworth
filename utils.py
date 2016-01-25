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
