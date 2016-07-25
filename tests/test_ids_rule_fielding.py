#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import time
import os

from nose.tools import *
from peewee import IntegrityError

from . import setup_each, teardown_each
from farnsworth.models.challenge_set import ChallengeSet
from farnsworth.models.ids_rule import IDSRule
from farnsworth.models.ids_rule_fielding import IDSRuleFielding
from farnsworth.models.round import Round
from farnsworth.models.team import Team


class TestIDSRuleFielding:

    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_latest(self):
        team1 = Team.create(name=Team.OUR_NAME)
        team2 = Team.create(name="other_team")
        cs = ChallengeSet.create(name="foo")

        ids1 = IDSRule.create(cs=cs, rules="ids1", sha256="sum1")
        ids2 = IDSRule.create(cs=cs, rules="ids2", sha256="sum2")
        ids3 = IDSRule.create(cs=cs, rules="ids3", sha256="sum3")

        r1 = Round.create(num=1)
        idsrf11 = IDSRuleFielding.create(cs=cs, ids_rule=ids1, team=team1, available_round=r1)
        idsrf12 = IDSRuleFielding.create(cs=cs, ids_rule=ids1, team=team2, available_round=r1)
        assert_equals(idsrf11, IDSRuleFielding.latest(cs, team1))
        assert_equals(idsrf12, IDSRuleFielding.latest(cs, team2))

        r2 = Round.create(num=2)
        idsrf21 = IDSRuleFielding.create(cs=cs, ids_rule=ids1, team=team1, available_round=r2)
        idsrf22 = IDSRuleFielding.create(cs=cs, ids_rule=ids2, team=team2, available_round=r2)
        assert_equals(idsrf21, IDSRuleFielding.latest(cs, team1))
        assert_equals(idsrf22, IDSRuleFielding.latest(cs, team2))

        r3 = Round.create(num=3)
        idsrf31 = IDSRuleFielding.create(cs=cs, ids_rule=ids3, team=team1, available_round=r3)
        idsrf32 = IDSRuleFielding.create(cs=cs, ids_rule=ids2, team=team2, available_round=r3)
        assert_equals(idsrf31, IDSRuleFielding.latest(cs, team1))
        assert_equals(idsrf32, IDSRuleFielding.latest(cs, team2))
