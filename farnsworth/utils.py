#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Various utility functions"""

from __future__ import absolute_import, unicode_literals

import re


def camel_case_to_underscore(string):
    """CamelCaseString => camel_case_string"""
    s1 = re.sub('([A-Z]+)([A-Z][a-z]+)', r'\1_\2', string)   # pylint:disable=invalid-name
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def stupid_pluralize(string):
    """Computer => Computers"""
    return string + "s"

def table_name(cls):
    """TableModel => table_models"""
    return stupid_pluralize(camel_case_to_underscore(cls.__name__))
