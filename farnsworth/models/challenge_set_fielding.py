#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os
import hashlib

from peewee import FixedCharField, ForeignKeyField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set import ChallengeSet
from .round import Round
from .team import Team

"""ChallengeSetFielding model"""


def _sha256sum(*strings):
    array = list(strings)
    array.sort()
    return hashlib.sha256("".join(array)).hexdigest()


class ChallengeSetFielding(BaseModel):
    """ChallengeSetFielding model"""

    cs = ForeignKeyField(ChallengeSet, related_name='fieldings')
    team = ForeignKeyField(Team, related_name='cs_fieldings')
    submission_round = ForeignKeyField(Round, related_name='cs_fieldings', null=True)
    available_round = ForeignKeyField(Round, related_name='cs_fieldings', null=True)
    fielded_round = ForeignKeyField(Round, related_name='cs_fieldings', null=True)
    cbns = ManyToManyField(ChallengeBinaryNode, related_name='cbns')
    sha256 = FixedCharField(max_length=64)

    @classmethod
    def create(cls, *args, **kwargs):
        if 'cbns' in kwargs:
            cbns = kwargs.pop('cbns')

        if 'sha256' not in kwargs:
            kwargs['sha256'] = _sha256sum(*[c.sha256 for c in cbns])

        obj = super(cls, cls).create(*args, **kwargs)
        obj.cbns = cbns
        return obj

    def add_cbns_if_missing(self, *cbns):
        """Wrap manytomany.add() to recalculate sha256 sum"""
        for cbn in cbns:
            if cbn not in self.cbns:
                self.cbns.add(cbns)
                self.sha256 = _sha256sum(*[c.sha256 for c in self.cbns])
        if self.is_dirty():
            self.save()

    @classmethod
    def latest(cls, cs, team):
        """
            Get latest cs fielding for provided team and CS
        :param cs: CS for which fielding need to be fetched.
        :param team: Team for which cs fielding need to be fetched.
        :return: list containing latest cs fielding.
        """

        query = ChallengeSetFielding.select()
        predicate = (ChallengeSetFielding.team == team) \
                    & (ChallengeSetFielding.cs == cs) \
                    & (ChallengeSetFielding.available_round == Round.current_round())
        return query.where(predicate).limit(1)
