#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import time
import os

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import (ChallengeBinaryNode, ChallengeBinaryNodeFielding,
                               ChallengeSet, Exploit, IDSRule, RexJob, Round, Team)


class TestChallengeSet:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_unsubmitted_ids_rules(self):
        cs = ChallengeSet.create(name="foo")
        ids1 = IDSRule.create(cs=cs, rules="aaa")
        ids2 = IDSRule.create(cs=cs, rules="bbb", submitted_at=datetime.now())

    def test_fielded_in_round(self):
        now = datetime.now()
        r1 = Round.create(num=0, ends_at=now + timedelta(seconds=15))
        r2 = Round.create(num=1, ends_at=now + timedelta(seconds=30))
        cs1 = ChallengeSet.create(name="foo")
        cs1.rounds = [r1, r2]
        cs2 = ChallengeSet.create(name="bar")
        cs2.rounds = [r1]

        assert_equals(len(ChallengeSet.fielded_in_round(r1)), 2)
        assert_in(cs1, ChallengeSet.fielded_in_round(r1))
        assert_in(cs2, ChallengeSet.fielded_in_round(r1))

    def test_cbns_by_patch_type(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum")
        cbn1 = ChallengeBinaryNode.create(name="foo1", cs=cs, patch_type="patch0", sha256="sum1")
        cbn2 = ChallengeBinaryNode.create(name="foo2", cs=cs, patch_type="patch0", sha256="sum2")
        cbn3 = ChallengeBinaryNode.create(name="foo3", cs=cs, patch_type="patch1", sha256="sum3")
        # FIXME: use assert_in
        assert_equals(['patch0', 'patch1'], sorted(cs.cbns_by_patch_type().keys()))
        assert_equals([cbn1, cbn2], cs.cbns_by_patch_type()['patch0'])
        assert_equals([cbn3], cs.cbns_by_patch_type()['patch1'])

    def test_unsubmitted_ids_rules(self):
        r1 = Round.create(num=0)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        ids1 = IDSRule.create(cs=cs, rules="aaa")
        ids2 = IDSRule.create(cs=cs, rules="bbb")

        assert_equals(len(cs.unsubmitted_ids_rules), 2)
        assert_in(ids1, cs.unsubmitted_ids_rules)
        assert_in(ids2, cs.unsubmitted_ids_rules)

        ids1.submit()
        assert_equals(len(cs.unsubmitted_ids_rules), 1)
        assert_not_in(ids1, cs.unsubmitted_ids_rules)
        assert_in(ids2, cs.unsubmitted_ids_rules)

        ids2.submit()
        assert_equals(len(cs.unsubmitted_ids_rules), 0)
        assert_not_in(ids1, cs.unsubmitted_ids_rules)
        assert_not_in(ids2, cs.unsubmitted_ids_rules)

    def test_unsubmitted_exploits(self):
        r1 = Round.create(num=0)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        cs.rounds = [r1]
        cbn = ChallengeBinaryNode.create(name="cbn", cs=cs, sha256="sum1")
        job = RexJob.create(cbn=cbn)
        pov1 = Exploit.create(cbn=cbn, job=job, pov_type='type1', exploitation_method='rop',
                              blob="exploit", c_code="exploit it")
        pov2 = Exploit.create(cbn=cbn, job=job, pov_type='type2', exploitation_method='rop',
                              blob="exploit", c_code="exploit it")

        assert_equals(len(cs.unsubmitted_exploits), 2)
        assert_in(pov1, cs.unsubmitted_exploits)
        assert_in(pov2, cs.unsubmitted_exploits)

        pov1.submit_to(team, 10)
        assert_equals(len(cs.unsubmitted_exploits), 1)
        assert_not_in(pov1, cs.unsubmitted_exploits)
        assert_in(pov2, cs.unsubmitted_exploits)

        pov2.submit_to(team, 10)
        assert_equals(len(cs.unsubmitted_exploits), 0)
        assert_not_in(pov1, cs.unsubmitted_exploits)
        assert_not_in(pov2, cs.unsubmitted_exploits)

    def test_cbns_unpatched(self):
        r0 = Round.create(num=0)
        r1 = Round.create(num=1)
        our_team = Team.create(name=Team.OUR_NAME)
        other_team = Team.create(name="opponent")
        cs = ChallengeSet.create(name="foo")
        cs.rounds = [r0, r1]
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum1")
        cbn_patched = ChallengeBinaryNode.create(name="foo", cs=cs, patch_type="patch0", sha256="sum2")
        cbn_other_team = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum3")
        ChallengeBinaryNodeFielding.create(cbn=cbn, team=our_team, available_round=r0)
        ChallengeBinaryNodeFielding.create(cbn=cbn_patched, team=our_team, submission_round=r0)
        ChallengeBinaryNodeFielding.create(cbn=cbn_other_team, team=other_team, available_round=r0)

        assert_equals(len(cs.cbns_unpatched), 1)
        assert_in(cbn, cs.cbns_unpatched)
        assert_not_in(cbn_patched, cs.cbns_unpatched)
        assert_not_in(cbn_other_team, cs.cbns_unpatched)

    def test_is_multi_cbn(self):
        r0 = Round.create(num=0)
        our_team = Team.create(name=Team.OUR_NAME)
        # CS single binary
        cs = ChallengeSet.create(name="single")
        cs.rounds = [r0]
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum1")
        # CS multi binary
        cs_multi = ChallengeSet.create(name="multi")
        cs_multi.rounds = [r0]
        cbn1 = ChallengeBinaryNode.create(name="foo1", cs=cs_multi, sha256="sum2")
        cbn2 = ChallengeBinaryNode.create(name="foo2", cs=cs_multi, sha256="sum3")
        # create fielding entries
        ChallengeBinaryNodeFielding.create(cbn=cbn, team=our_team, available_round=r0)
        ChallengeBinaryNodeFielding.create(cbn=cbn1, team=our_team, available_round=r0)
        ChallengeBinaryNodeFielding.create(cbn=cbn2, team=our_team, available_round=r0)

        assert_false(cs.is_multi_cbn)
        assert_true(cs_multi.is_multi_cbn)
>>>>>>> dacd9e93256294f75f3ab8c2053e89db4417903a
