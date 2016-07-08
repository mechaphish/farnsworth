#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import Field

"""Extend Peewee basic types."""


class EnumField(Field):
    """Define a EnumField type"""
    db_field = "enum"

    def pre_field_create(self, model):
        cursor = self.get_database().get_conn().cursor()
        choices_str = ", ".join(itertools.repeat("'%s'", len(self.choices))
        cursor.execute("CREATE TYPE %s AS ENUM ({});".format(choices_str),
                       (self.db_field, ) + tuple(self.choices))

    def coerce(self, value):
        if value not in self.choices:
            raise Exception("Invalid Enum Value `%s`", value)
        return str(value)

    def get_column_type(self):
        return "enum"
