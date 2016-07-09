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

    ids_rule = ForeignKeyField(IDSRule, db_column='ids_rule_id', related_name='fieldings',
                               null=False)
    team = ForeignKeyField(Team, db_column='team_id', related_name='fieldings', null=False)
    submission_round = ForeignKeyField(Round, db_column='submission_round_id',
                                       related_name='fieldings', null=False)
    available_round = ForeignKeyField(Round, db_column='available_round_id',
                                      related_name='fieldings', null=True)
    fielded_round = ForeignKeyField(Round, db_column='fielded_round_id', related_name='fieldings',
                                    null=True)
