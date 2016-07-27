#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Feedback model"""

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField, FloatField

from .base import BaseModel
from .round import Round
from .challenge_set import ChallengeSet
from .concerns.round_related_model import RoundRelatedModel
from ..mixins.cb_score_mixin import CBScoreMixin


class PollFeedback(BaseModel, RoundRelatedModel, CBScoreMixin):
    """Feedback model"""
    cs = ForeignKeyField(ChallengeSet, related_name='feedbacks')
    round = ForeignKeyField(Round, related_name='poll_feedbacks')

    # functionality tests
    success = FloatField()
    timeout = FloatField()
    connect = FloatField()
    function = FloatField()

    # performance tests
    time_overhead = FloatField()
    memory_overhead = FloatField()

    @property
    def cbns(self):
        return self.cs_fielding.get().cbns

    @property
    def patch_type(self):
        return self.cbns.get().patch_type

    # security
    @property
    def security(self):
        pt = self.patch_type
        if pt is None:
            # unpatched
            return 1
        else:
            return 2 - self.patch_type.exploitability

    @property
    def cbns(self):
        return self.cs_fielding.get().cbns

    @property
    def size_overhead(self):
        current_size = sum(cbn.size for cbn in self.cbns)
        orig_size = sum(cbn.size for cbn in self.cs.cbns_original)
        return max(float(current_size) / float(orig_size) - 1.0, 0.0)
