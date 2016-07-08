#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import CharField

from .base import BaseModel

"""Team model"""


class Team(BaseModel):
    """Team model"""
    name = CharField()

    @classmethod
    def opponents(cls):
        """Return oppenent teams"""
        return cls.select().where(cls.name != "6")
