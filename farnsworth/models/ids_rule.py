#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import hashlib

from peewee import FixedCharField, ForeignKeyField, TextField

from .base import BaseModel
from .challenge_set import ChallengeSet

"""IDSRule model"""


class IDSRule(BaseModel):
    """IDSRule model"""
    cs = ForeignKeyField(ChallengeSet, related_name='ids_rules')
    rules = TextField()
    sha256 = FixedCharField(max_length=64)

    def save(self, **kwargs):
        if self.sha256 is None:
            self.sha256 = hashlib.sha256(self.rules).hexdigest()
        return super(IDSRule, self).save(**kwargs)

    @classmethod
    def get_by_sha256_or_create(cls, **kwargs):
        sha256 = hashlib.sha256(kwargs['rules']).hexdigest()
        try:
            return cls.get(cls.sha256 == sha256)
        except cls.DoesNotExist:
            return cls.create(sha256=sha256, **kwargs)
