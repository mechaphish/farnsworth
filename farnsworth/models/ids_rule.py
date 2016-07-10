#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from peewee import ForeignKeyField, TextField

from .base import BaseModel
from .challenge_set import ChallengeSet

"""IDSRule model"""


class IDSRule(BaseModel):
    """IDSRule model"""
    cs = ForeignKeyField(ChallengeSet, related_name='ids_rules')
    rules = TextField()

    def submit(self):
        """Save submission at current round"""
        from .ids_rule_fielding import IDSRuleFielding
        from .round import Round
        from .team import Team
        irf = IDSRuleFielding.create(ids_rule=self, submission_round=Round.get_current(),
                                     team=Team.get_our())
