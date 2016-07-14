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
