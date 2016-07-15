#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import IntegerField, TextField, ForeignKeyField

from .base import BaseModel
from .exploit import Exploit
from .challenge_set_fielding import ChallengeSetFielding
from .ids_rule_fielding import IDSRuleFielding

"""PovTestResult model"""


class PovTestResult(BaseModel):
    """
    Result of a Pov Tested against a team with an ids_rules.
    """
    exploit = ForeignKeyField(Exploit, related_name='pov_test_results')
    cs_fielding = ForeignKeyField(ChallengeSetFielding, related_name='cs_fielding')
    ids_fielding = ForeignKeyField(IDSRuleFielding, related_name='ids_fielding', null=True)
    # Number of times Pov Succeeded out of 10 throws.
    num_success = IntegerField(default=0)
    # Feedback from Pov Testing, this could be used by Pov Fuzzer.
    test_feedback = TextField(null=True)
