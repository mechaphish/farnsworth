#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField, IntegerField, FloatField, BooleanField

from .base import BaseModel
from .round import Round
from .team import Team
from .challenge_set import ChallengeSet
from .concerns.round_related_model import RoundRelatedModel
from ..mixins import CBScoreMixin

"""Feedback model"""


class PollFeedback(BaseModel, RoundRelatedModel, CBScoreMixin):
    """Feedback model"""
    cs = ForeignKeyField(ChallengeSet, related_name='feedbacks')

    #round = ForeignKeyField(Round, related_name='feedbacks')
    round_id = IntegerField()
    @property
    def round(self):
        return Round.get(id=self.round_id)

    @property
    def cbns(self):
        return self.cs_fielding.get().cbns

    @property
    def patch_type(self):
        return self.cbns.get().patch_type

    # functionality tests
    success = FloatField()
    timeout = FloatField()
    connect = FloatField()
    function = FloatField()

    # performance tests
    time_overhead = FloatField()
    memory_overhead = FloatField()
    size_overhead = FloatField()

    # security
    @property
    def security(self):
        pt = self.patch_type
        if pt is None:
            # unpatched
            return 1
        else:
            return 2 - self.patch_type.exploitability
