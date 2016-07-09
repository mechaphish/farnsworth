#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BooleanField, ForeignKeyField, CharField, BigIntegerField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .round import Round
from .challenge_set import ChallengeSet

"""patch_scores model"""


class PatchScore(BaseModel):
    """
    Score of a patched CB
    """
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='patch_scores')
    patch_type = CharField(null=True)
    num_polls = BigIntegerField(null=False)
    polls_included = BinaryJSONField(null=True)
    has_failed_polls = BooleanField(null=False, default=False)
    failed_polls = BinaryJSONField(null=True)
    round = ForeignKeyField(Round, db_column='round_id', related_name='patch_scores')
    perf_score = BinaryJSONField(null=False)
