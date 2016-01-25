#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A collection of utilities to make developing easier :)
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"

import functools
import json


def jsonify(func):
    """Decorator to jsonify return values of functions.

    :param function func: Function wrapped to return JSON instead of Python objects.
    """
    @functools.wraps(func)
    def wrapper(**kwds):     # pylint: disable=missing-docstring
        return json.dumps(func(**kwds))
    return wrapper
