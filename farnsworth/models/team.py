#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import CharField

from .base import BaseModel

"""Team model"""


class Team(BaseModel):
    """Team model"""
    OUR_NAME = "6"

    name = CharField()

    @classmethod
    def get_our(cls):
        """Return our team"""
        return cls.get(cls.name == cls.OUR_NAME)

    @classmethod
    def opponents(cls):
        """Return opponent teams"""
        return cls.select().where(cls.name != cls.OUR_NAME)
