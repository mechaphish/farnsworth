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

    cbn = ForeignKeyField(ChallengeBinaryNode, related_name='fieldings')
    team = ForeignKeyField(Team, related_name='cbn_fieldings')
    submission_round = ForeignKeyField(Round, related_name='cbn_fieldings', null=True)
    available_round = ForeignKeyField(Round, related_name='cbn_fieldings', null=True)
    fielded_round = ForeignKeyField(Round, related_name='cbn_fieldings', null=True)
