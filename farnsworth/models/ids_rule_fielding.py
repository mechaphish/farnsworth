#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from peewee import ForeignKeyField

from .base import BaseModel
from .ids_rule import IDSRule
from .round import Round
from .team import Team

"""IDSRuleFielding model"""


class IDSRuleFielding(BaseModel):
    """IDSRuleFielding model"""

    ids_rule = ForeignKeyField(IDSRule, related_name='fieldings')
    team = ForeignKeyField(Team, related_name='ids_fieldings')
    submission_round = ForeignKeyField(Round, related_name='ids_fieldings')
    available_round = ForeignKeyField(Round, related_name='ids_fieldings', null=True)
    fielded_round = ForeignKeyField(Round, related_name='ids_fieldings', null=True)
