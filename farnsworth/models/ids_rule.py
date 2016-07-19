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
    sha256 = FixedCharField(max_length=64) # this index shit doesn't work, we create it manually

    def submit(self, round=None):
        """Save submission at specified round. If None use current round."""
        from .ids_rule_fielding import IDSRuleFielding
        from .round import Round
        from .team import Team
        if round is None:
            round = Round.current_round()
        return IDSRuleFielding.create(ids_rule=self,
                                      submission_round=round,
                                      team=Team.get_our())

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
            kwargs['sha256'] = sha256
            return cls.create(**kwargs)
