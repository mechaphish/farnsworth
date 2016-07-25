#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BooleanField, CharField, ForeignKeyField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .valid_polls import ValidPoll
from .patch_type import PatchType
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
    patch_type = ForeignKeyField(PatchType, related_name='cb_poll_performances', null=True)

    @classmethod
    def num_tested_polls(cls, cs, patch_type):
        """
            Get number of tested polls on the provided CS and patch type
        :param cs: Challenge Set for num successful polls tested.
        :param patch_type: Patch Type for which results need to be fetched.
        :return: num of tested polls
        """
        if patch_type is None:
            return CBPollPerformance.select() \
                                    .where(CBPollPerformance.cs == cs,
                                           CBPollPerformance.patch_type.is_null(True)).count()
        else:
            return CBPollPerformance.select() \
                                    .where(CBPollPerformance.cs == cs,
                                           CBPollPerformance.patch_type == patch_type).count()

    @classmethod
    def get_untested_polls(cls, cs, patch_type):
        """
            Get list of untested polls for provided CS and patch type
        :param cs: Challenge Set for which untested polls need to be fetched.
        :param patch_type: Patch Type for which untested polls need to be fetched.
        :return: all untested polls for provided CS and patch type
        """
        if patch_type is None:
            tested_polls = CBPollPerformance.select(CBPollPerformance.poll) \
                                            .where(CBPollPerformance.cs == cs,
                                                   CBPollPerformance.patch_type.is_null(True))
        else:
            tested_polls = CBPollPerformance.select(CBPollPerformance.poll) \
                                            .where(CBPollPerformance.cs == cs,
                                                   CBPollPerformance.patch_type == patch_type)
        return cs.valid_polls.where(ValidPoll.id.not_in(tested_polls))
