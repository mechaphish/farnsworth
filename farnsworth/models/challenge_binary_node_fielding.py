#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from peewee import ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .round import Round
from .team import Team

"""ChallengeBinaryNodeFielding model"""


class ChallengeBinaryNodeFielding(BaseModel):
    """ChallengeBinaryNodeFielding model"""

    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='fieldings',
                          null=False)
    team = ForeignKeyField(Team, db_column='team_id', related_name='fieldings', null=False)
    submission_round = ForeignKeyField(Round, db_column='submission_round_id',
                                       related_name='fieldings', null=True)
    available_round = ForeignKeyField(Round, db_column='available_round_id',
                                      related_name='fieldings', null=True)
    fielded_round = ForeignKeyField(Round, db_column='fielded_round_id', related_name='fieldings',
                                    null=True)
