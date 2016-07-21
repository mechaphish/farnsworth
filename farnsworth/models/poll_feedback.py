#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField, IntegerField, FloatField

from .base import BaseModel
from .round import Round
from .team import Team
from .challenge_set import ChallengeSet
from .challenge_set_fielding import ChallengeSetFielding
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
    def cs_fielding(self):
        our_team = Team.get_our()
        return ChallengeSetFielding.select().where(
            (ChallengeSetFielding.available_round == self.round) &
            (ChallengeSetFielding.team == our_team) &
            (ChallengeSetFielding.cs == self.cs)
        )[0]

    @property
    def cbns(self):
        return self.cs_fielding.cbns

    @property
    def patch_type(self):
        return self.cbns[0].patch_type

    @property
    def fielding(self):
        """
        Returns which fielding this is for.
        """
        return ChallengeSetFielding.select().where(
            ChallengeSetFielding.fielded_round == PollFeedback.round &
            ChallengeSetFielding.cs == PollFeedback.cs
        )

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
            return 1 - self.patch_type.exploitability
