#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import time
import os

from nose.tools import *
from peewee import IntegrityError

from . import setup_each, teardown_each
from farnsworth.models import (ChallengeBinaryNode, ChallengeSet, ChallengeSetFielding,
                               Round, Team)


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
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, sha256="sum1")
        cbn2 = ChallengeBinaryNode.create(name="foo_2", cs=cs, sha256="sum2")

        csf = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r0)
        assert_equals(csf.sha256, "bb558b4638d76b2461f5cdeca98bc8b4ba29b652cfa1ca7662c82d15fd171063")

        csf2 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1, cbn2], team=team, available_round=r1)
        assert_equals(csf2.sha256, "9f8525c7dceee7e6c7a505d0a18bb22082dfa11cec5ade586e46fe77c4564047")

        # insert duplicate team+cs+round fails
        assert_raises(IntegrityError, ChallengeSetFielding.create, cs=cs, cbns=[cbn1], team=team, available_round=r0)

    def test_add_cbns_if_missing(self):
        r0 = Round.create(num=0)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, sha256="sum1")
        cbn2 = ChallengeBinaryNode.create(name="foo_2", cs=cs, sha256="sum2")
        cbn3 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum3")
        csf = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r0)
        assert_equals(len(csf.cbns), 1)
        assert_equals(csf.sha256, "bb558b4638d76b2461f5cdeca98bc8b4ba29b652cfa1ca7662c82d15fd171063")

        csf.add_cbns_if_missing(cbn2, cbn3)
        assert_equals(len(csf.cbns), 3)
        assert_equals(csf.sha256, "647dceb057c2155895174a2915c6b54f7790785b3b1ab1fe2b399e7e1b5b0889")

        csf.add_cbns_if_missing(cbn2, cbn3)
        assert_equals(len(csf.cbns), 3)
        assert_equals(csf.sha256, "647dceb057c2155895174a2915c6b54f7790785b3b1ab1fe2b399e7e1b5b0889")
