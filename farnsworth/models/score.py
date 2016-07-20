#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .concerns.round_related_model import RoundRelatedModel
from .round import Round

"""Score model"""


class Score(BaseModel, RoundRelatedModel):
    """Score model"""
    round = ForeignKeyField(Round, related_name='scores')
    scores = BinaryJSONField()
