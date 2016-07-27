#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""ChallengeSetFielding model"""

from __future__ import absolute_import, unicode_literals

import hashlib

from peewee import FixedCharField, ForeignKeyField, FloatField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set import ChallengeSet
from .round import Round
from .team import Team
from .poll_feedback import PollFeedback


def _sha256sum(*strings):
    array = list(strings)
    array.sort()
    return hashlib.sha256("".join(array)).hexdigest()


class ChallengeSetFielding(BaseModel):
    """ChallengeSetFielding model"""

    cs = ForeignKeyField(ChallengeSet, related_name='fieldings')
    team = ForeignKeyField(Team, related_name='cs_fieldings')
    submission_round = ForeignKeyField(Round, related_name='submitted_fieldings', null=True)
    available_round = ForeignKeyField(Round, related_name='available_fieldings', null=True)
    cbns = ManyToManyField(ChallengeBinaryNode, related_name='fieldings')
    sha256 = FixedCharField(max_length=64)
    remote_cb_score = FloatField(null=True)  # performance metric computed from feedback from DARPA.

    poll_feedback = ForeignKeyField(PollFeedback, related_name='cs_fielding', null=True)

    @classmethod
    def create(cls, *args, **kwargs):
        if 'cbns' in kwargs:
            cbns = kwargs.pop('cbns')
            if 'sha256' not in kwargs:
                kwargs['sha256'] = _sha256sum(*[c.sha256 for c in cbns])

        obj = super(cls, cls).create(*args, **kwargs)
        obj.cbns = cbns
        return obj

    @classmethod
    def create_or_update_submission(cls, team, cbns, round=None):
        try:
            csf = cls.get((cls.cs == cbns[0].cs) & \
                          (cls.team == team) & \
                          (cls.submission_round == round))
            csf.replace_cbns(cbns)
        except cls.DoesNotExist:
            csf = cls.create(cs=cbns[0].cs, team=team, cbns=cbns, submission_round=round)
        return csf

    @classmethod
    def create_or_update_available(cls, team, cbn, round=None):
        try:
            csf = cls.get((cls.cs == cbn.cs) & \
                          (cls.team == team) & \
                          (cls.available_round == round))
            csf.add_cbns_if_missing(cbn)
        except cls.DoesNotExist:
            csf = cls.create(cs=cbn.cs, team=team, cbns=[cbn], available_round=round)
        return csf

    def replace_cbns(self, cbns):
        self.cbns = cbns
        self.sha256 = _sha256sum(*[c.sha256 for c in self.cbns])
        if self.is_dirty():
            self.save()

    def add_cbns_if_missing(self, *cbns):
        """Wrap manytomany.add() to recalculate sha256 sum"""
        for cbn in cbns:
            if cbn not in self.cbns:
                self.cbns.add(cbns)
                self.sha256 = _sha256sum(*[c.sha256 for c in self.cbns])
        if self.is_dirty():
            self.save()

    @classmethod
    def latest(cls, cs, team, round=None):
        """
            Get latest cs fielding for provided team and CS
        :param cs: CS for which fielding need to be fetched.
        :param team: Team for which cs fielding need to be fetched.
        :return: list containing latest cs fielding.
        """
        if round is None:
            round = Round.current_round()

        try:
            return cls.get((cls.cs == cs)
                           & (cls.team == team)
                           & (cls.available_round == round))
        except cls.DoesNotExist:
            return

    @classmethod
    def submissions(cls, cs, team, round=None):
        if round is None:
            round = Round.current_round()

        try:
            return cls.get((cls.cs == cs)
                           & (cls.team == team)
                           & (cls.submission_round == round))
        except cls.DoesNotExist:
            return
