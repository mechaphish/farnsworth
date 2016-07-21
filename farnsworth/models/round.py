#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import DateTimeField, IntegerField

from .base import BaseModel

"""Round model"""


class Round(BaseModel):
    """Round model."""
    ends_at = DateTimeField(null=True)
    num = IntegerField()

    @classmethod
    def prev_round(cls):
        rounds = cls.select().order_by(cls.created_at.desc())
        if len(rounds) > 1:
            return rounds[1]

    @classmethod
    def current_round(cls):
        rounds = cls.select().order_by(cls.created_at.desc())
        if rounds:
            return rounds[0]

    @classmethod
    def at_timestamp(cls, timestamp):
        DeprecationWarning("This method is useless. It will be removed soon.")
        rounds = cls.select().where(cls.created_at < timestamp) \
                    .order_by(cls.created_at.desc()).limit(1)
        if rounds:
            return rounds[0]
