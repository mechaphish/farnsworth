#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from peewee import ForeignKeyField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .round import Round
from .team import Team

"""Evaluation model"""


class Evaluation(BaseModel):
    """Evaluation model"""
    round = ForeignKeyField(Round, related_name='evaluations')
    team = ForeignKeyField(Team, related_name='evaluations')
    ids = BinaryJSONField()
    cbs = BinaryJSONField()

    @classmethod
    def update_or_create(cls, round_, team, **kwargs):
        """Update or create evaluation"""
        update = cls.update(updated_at=datetime.now(),
                            **kwargs).where(cls.round == round_,
                                            cls.team == team)
        if update.execute() == 0:
            cls.create(round=round_, team=team, **kwargs)
