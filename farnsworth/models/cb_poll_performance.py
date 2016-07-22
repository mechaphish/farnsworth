#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BooleanField, CharField, ForeignKeyField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .valid_polls import ValidPoll
from .challenge_set import ChallengeSet

"""cb_poll_performances model"""


class CBPollPerformance(BaseModel):
    """
    Performance of a CB against a poll.
    """
    cs = ForeignKeyField(ChallengeSet, related_name='cb_poll_performances')
    poll = ForeignKeyField(ValidPoll, related_name='cb_poll_performances')
    performances = BinaryJSONField()
    is_poll_ok = BooleanField(default=False)
    patch_type = CharField(null=True)   # THIS SHOULD NOT BE A CHARFIELD

    @classmethod
    def num_success_polls(cs, patch_type):
        """
            Get number of successful polls tested on the provided CS and patch type
        :param target_cs: Challenge Set for num successful polls tested.
        :param patch_type: Patch Type for which results need to be fetched.
        :return: num of successful polls
        """
        if patch_type is None:
            return CBPollPerformance.select() \
                                    .where(CBPollPerformance.cs == cs
                                           & CBPollPerformance.patch_type.is_null(True)
                                           & CBPollPerformance.is_poll_ok == True).count()
        else:
            return CBPollPerformance.select() \
                                    .where(CBPollPerformance.cs == cs
                                           & CBPollPerformance.patch_type == patch_type
                                           & CBPollPerformance.is_poll_ok == True).count()
