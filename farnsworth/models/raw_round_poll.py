#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField, BooleanField, BlobField
from playhouse.postgres_ext import BlobField

from .round import Round
from .base import BaseModel
from .challenge_set import ChallengeSet

"""RawRoundPoll model"""


class RawRoundPoll(BaseModel):
    """
    Poll created from network traffic.
    """
    round = ForeignKeyField(Round, related_name='raw_round_polls')
    is_crash = BooleanField(null=False, default=False)
    is_failed = BooleanField(null=False, default=False)
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='raw_round_polls')
    blob = BlobField(null=False)
    sanitized = BooleanField(null=False, default=False)
