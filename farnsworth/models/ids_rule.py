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

    def submit(self):
        """Save submission at current round"""
        from .ids_rule_fielding import IDSRuleFielding
        from .round import Round
        from .team import Team
        irf = IDSRuleFielding.create(ids_rule=self, submission_round=Round.current_round(),
                                     team=Team.get_our())

    def save(self, **kwargs):
        if self.sha256 is None:
            self.sha256 = hashlib.sha256(self.rules).hexdigest()
        return super(IDSRule, self).save(**kwargs)
