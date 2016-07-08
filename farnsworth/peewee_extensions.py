#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import Field, SQL

import itertools

"""Extend Peewee basic types."""


class EnumField(Field):
    """Define a EnumField type"""
    db_field = "enum"

    def __init__(self, *args, **kwargs):
        self.enum_name = kwargs.pop('enum_name')
        super(self.__class__, self).__init__(*args, **kwargs)

    def pre_field_create(self, model):
        cursor = self.get_database().get_conn().cursor()
        cursor.execute("DROP TYPE IF EXISTS {};".format(self.enum_name))
        choices_str = ", ".join(itertools.repeat("%s", len(self.choices)))
        query = "CREATE TYPE {} AS ENUM ({});".format(self.enum_name, choices_str)
        cursor.execute(query, self.choices)
        self.db_field = self.enum_name

    def coerce(self, value):
        if value not in self.choices:
            raise Exception("Invalid Enum Value `%s`", value)
        return str(value)

    def get_column_type(self):
        return "enum"

    def __ddl_column__(self, ctype):
        return SQL(self.enum_name)
