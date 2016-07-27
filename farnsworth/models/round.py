#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Round model"""

from __future__ import absolute_import, unicode_literals

from datetime import datetime
from peewee import DateTimeField, IntegerField

from .base import BaseModel


class Round(BaseModel):
    """Round model."""
    num = IntegerField()
    ready_at = DateTimeField(null=True)

    @classmethod
    def prev_round(cls):
        rounds = cls.select().order_by(cls.created_at.desc()).limit(1).offset(1)
        if rounds:
            if rounds[0].num < cls.current_round().num:
                return rounds[0]
            # Otherwise, we might be in a new game

    @classmethod
    def current_round(cls):
        rounds = cls.select().order_by(cls.created_at.desc()).limit(1)
        if rounds:
            return rounds[0]

    @classmethod
    def at_timestamp(cls, timestamp):
        DeprecationWarning("This method is useless. It will be removed soon.")
        rounds = cls.select().where(cls.created_at < timestamp) \
                    .order_by(cls.created_at.desc()).limit(1)
        if rounds:
            return rounds[0]

    def ready(self):
        self.ready_at = datetime.now()
        self.save()

    def is_ready(self):
        return (self.ready_at is not None)
