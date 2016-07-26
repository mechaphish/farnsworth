#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import time
import os

from nose.tools import *
from peewee import IntegrityError

from . import setup_each, teardown_each
from farnsworth.models.challenge_binary_node import ChallengeBinaryNode
from farnsworth.models.challenge_set import ChallengeSet
from farnsworth.models.challenge_set_fielding import ChallengeSetFielding
from farnsworth.models.round import Round
from farnsworth.models.team import Team


class TestChallengeSetFielding:

    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_create(self):
        r0 = Round.create(num=0)
        r1 = Round.create(num=1)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, blob="aaa1")
        cbn2 = ChallengeBinaryNode.create(name="foo_2", cs=cs, blob="aaa2")

        csf = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r0)
        assert_equals(csf.sha256, "04de190c8dbd04bdb5768118c2cd745c7918f6858eddd765354819fc59c6d46e")

        csf2 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1, cbn2], team=team, available_round=r1)
        assert_equals(csf2.sha256, "277b0b746f1937a8f54797e2698e54f8646f0413ad353da19d93522c05817e73")

        # insert duplicate team+cs+round fails
        assert_raises(IntegrityError, ChallengeSetFielding.create, cs=cs, cbns=[cbn1], team=team,
                      available_round=r0)

    def create_or_update(self):
        r0 = Round.create(num=0)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, blob="aaa1")
        cbn2 = ChallengeBinaryNode.create(name="foo_2", cs=cs, blob="aaa2")

        csf1 = ChallengeSetFielding.create_or_update(team=team, round=r0, cbn=cbn1)
        assert_in(cbn1, csf1.cbns)
        assert_equals(len(csf1.cbns), 1)

        csf2 = ChallengeSetFielding.create_or_update(team=team, round=r0, cbn=cbn2)
        assert_equals(csf1, csf2)
        assert_in(cbn2, csf1.cbns)
        assert_equals(len(csf1.cbns), 2)

    def test_add_cbns_if_missing(self):
        r0 = Round.create(num=0)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, blob="aaa1")
        cbn2 = ChallengeBinaryNode.create(name="foo_2", cs=cs, blob="aaa2")
        cbn3 = ChallengeBinaryNode.create(name="foo_3", cs=cs, blob="aaa3")
        csf = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r0)
        assert_equals(len(csf.cbns), 1)
        assert_equals(csf.sha256, "04de190c8dbd04bdb5768118c2cd745c7918f6858eddd765354819fc59c6d46e")

        csf.add_cbns_if_missing(cbn2, cbn3)
        assert_equals(len(csf.cbns), 3)
        assert_equals(csf.sha256, "85b75a70a55b3e7606d1a1cc19ee1a16f1ad510dfb4dc84648a9df3ec6f83fe0")

        csf.add_cbns_if_missing(cbn2, cbn3)
        assert_equals(len(csf.cbns), 3)
        assert_equals(csf.sha256, "85b75a70a55b3e7606d1a1cc19ee1a16f1ad510dfb4dc84648a9df3ec6f83fe0")

    def test_latest(self):
        team1 = Team.create(name=Team.OUR_NAME)
        team2 = Team.create(name="other_team")
        cs = ChallengeSet.create(name="foo")

        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, sha256="sum1", blob="blob1")
        cbn2 = ChallengeBinaryNode.create(name="foo_2", cs=cs, sha256="sum2", blob="blob2")
        cbn3 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum3", blob="blob3")

        r1 = Round.create(num=1)
        csf11 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team1, available_round=r1)
        csf12 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team2, available_round=r1)
        assert_equals(csf11, ChallengeSetFielding.latest(cs, team1))
        assert_equals(csf12, ChallengeSetFielding.latest(cs, team2))

        r2 = Round.create(num=2)
        csf21 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team1, available_round=r2)
        csf22 = ChallengeSetFielding.create(cs=cs, cbns=[cbn2], team=team2, available_round=r2)
        assert_equals(csf21, ChallengeSetFielding.latest(cs, team1))
        assert_equals(csf22, ChallengeSetFielding.latest(cs, team2))

        r3 = Round.create(num=3)
        csf31 = ChallengeSetFielding.create(cs=cs, cbns=[cbn3], team=team1, available_round=r3)
        csf32 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team2, available_round=r3)
        assert_equals(csf31, ChallengeSetFielding.latest(cs, team1))
        assert_equals(csf32, ChallengeSetFielding.latest(cs, team2))
