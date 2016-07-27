#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""IDSRuleFielding model"""

from __future__ import absolute_import, unicode_literals

from peewee import FixedCharField, ForeignKeyField

from .base import BaseModel
from .ids_rule import IDSRule
from .round import Round
from .team import Team


class IDSRuleFielding(BaseModel):
    """IDSRuleFielding model"""

    ids_rule = ForeignKeyField(IDSRule, related_name='fieldings')
    team = ForeignKeyField(Team, related_name='ids_fieldings')
    submission_round = ForeignKeyField(Round, related_name='submitted_ids_fieldings', null=True)
    available_round = ForeignKeyField(Round, related_name='available_ids_fieldings', null=True)
    sha256 = FixedCharField(max_length=64, null=True) # FIXME

    @classmethod
    def latest(cls, cs, team):
        """Get latest IDS fielding for provided team and CS.

        :param cs: CS for which IDS fielding need to be fetched.
        :param team: Team for which IDS fielding need to be fetched.
        :return: list containing latest IDS fielding.
        """

        query = cls.select(cls).join(IDSRule, on=(cls.ids_rule == IDSRule.id))
        predicate = (IDSRule.cs == cs) \
                    & (cls.team == team) \
                    & (cls.available_round == Round.current_round())
        result = query.where(predicate).limit(1)
        if result:
            return result[0]
