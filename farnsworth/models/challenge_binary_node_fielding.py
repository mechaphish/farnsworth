#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from playhouse.fields import ManyToManyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .round import Round
from .team import Team

"""ChallengeBinaryNodeFielding model"""


class ChallengeBinaryNodeFielding(BaseModel):
    """ChallengeBinaryNodeFielding model"""

    cbn = ManyToManyField(ChallengeBinaryNode, related_name='fieldings')
    team = ManyToManyField(Team, related_name='cbn_fieldings')
    submission_round = ManyToManyField(Round, related_name='cbn_fieldings')
    available_round = ManyToManyField(Round, related_name='cbn_fieldings')
    fielded_round = ManyToManyField(Round, related_name='cbn_fieldings')
