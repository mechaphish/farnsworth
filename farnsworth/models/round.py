#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import DateTimeField, IntegerField

from .base import BaseModel

"""Round model"""


class Round(BaseModel):
    """Round model."""
    ends_at = DateTimeField()
    num = IntegerField()

    @classmethod
    def current_round(cls):
        return cls.select().order_by(cls.created_at.desc())[0]

    @classmethod
    def at_timestamp(cls, timestamp):
        rounds = cls.select().where(cls.created_at < timestamp).order_by(cls.created_at.desc())
        if rounds:
            return rounds[0]
