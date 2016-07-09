#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BooleanField, BlobField, ForeignKeyField
from playhouse.postgres_ext import BlobField

from .round import Round
from .base import BaseModel

"""RawRoundTraffic model"""


class RawRoundTraffic(BaseModel):
    """
    Result corresponding to the network dude
    """
    round = ForeignKeyField(Round, related_name='raw_round_traffics')
    processed = BooleanField(null=False, default=False)
    pickled_data = BlobField()
