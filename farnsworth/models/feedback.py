#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from playhouse.fields import ManyToManyField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .round import Round
from .round_related_model import RoundRelatedModel

"""Feedback model"""


class Feedback(BaseModel, RoundRelatedModel):
    """Feedback model"""
    round = ManyToManyField(Round, related_name='feedbacks')
    polls = BinaryJSONField()
    cbs = BinaryJSONField()
    povs = BinaryJSONField()
