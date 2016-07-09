#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from playhouse.fields import ManyToManyField

from .base import BaseModel
from .ids_rule import IDSRule
from .round import Round
from .team import Team

"""IDSRuleFielding model"""


class IDSRuleFielding(BaseModel):
    """IDSRuleFielding model"""

    ids_rule = ManyToManyField(IDSRule, related_name='fieldings')
    team = ManyToManyField(Team, related_name='ids_fieldings')
    submission_round = ManyToManyField(Round, related_name='ids_fieldings')
    available_round = ManyToManyField(Round, related_name='ids_fieldings')
    fielded_round = ManyToManyField(Round, related_name='ids_fieldings')
