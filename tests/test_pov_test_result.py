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
from farnsworth.models.exploit import Exploit
from farnsworth.models.ids_rule import IDSRule
from farnsworth.models.ids_rule_fielding import IDSRuleFielding
from farnsworth.models.job import AFLJob
from farnsworth.models.pov_test_result import PovTestResult
from farnsworth.models.round import Round
from farnsworth.models.team import Team

#
#    exploit = ForeignKeyField(Exploit, related_name='pov_test_results')
#    cs_fielding = ForeignKeyField(ChallengeSetFielding, related_name='cs_fielding')
#    ids_fielding = ForeignKeyField(IDSRuleFielding, related_name='ids_fielding', null=True)
#    # Number of times Pov Succeeded out of 10 throws.
#    num_success = IntegerField(default=0)
#    # Feedback from Pov Testing, this could be used by Pov Fuzzer.
#    test_feedback = TextField(null=True)
#

class TestPovTestResult:

    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_best(self):
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")

        r1 = Round.create(num=1)
        ids1 = IDSRule.create(cs=cs, rules="ids1", sha256="sum1")
        idsrf1 = IDSRuleFielding.create(cs=cs, ids_rule=ids1, team=team, available_round=r1)

        cbn1 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum3")
        csf1 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r1)

        r2 = Round.create(num=2)
        cbn2 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum4")
        csf2 = ChallengeSetFielding.create(cs=cs, cbns=[cbn2], team=team, available_round=r2)

        job = AFLJob.create(cbn=cbn1, cs=cs)
        exploit = Exploit.create(job=job, cs=cs, blob="exploit", pov_type='type1',
                                 c_code="c_code")

        assert_is_none(PovTestResult.best(csf1, idsrf1))

        pov1 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    num_success=2)
        assert_is_none(PovTestResult.best(csf1, idsrf1))
        assert_is_none(PovTestResult.best(csf2, idsrf1))

        pov2 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=2)
        assert_equals(pov2, PovTestResult.best(csf1, idsrf1))
        assert_is_none(PovTestResult.best(csf2, idsrf1))

        pov3 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=1)
        assert_equals(pov2, PovTestResult.best(csf1, idsrf1))
        assert_is_none(PovTestResult.best(csf2, idsrf1))

        pov4 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=4)
        pov5 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf2,
                                    ids_fielding=idsrf1,
                                    num_success=8)
        assert_equals(pov4, PovTestResult.best(csf1, idsrf1))
        assert_equals(pov5, PovTestResult.best(csf2, idsrf1))

    def test_best_against_cs_fielding(self):
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")

        r1 = Round.create(num=1)
        ids1 = IDSRule.create(cs=cs, rules="ids1", sha256="sum1")
        idsrf1 = IDSRuleFielding.create(cs=cs, ids_rule=ids1, team=team, available_round=r1)

        cbn1 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum3")
        csf1 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r1)

        r2 = Round.create(num=2)
        cbn2 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum4")
        csf2 = ChallengeSetFielding.create(cs=cs, cbns=[cbn2], team=team, available_round=r2)

        job = AFLJob.create(cbn=cbn1, cs=cs)
        exploit = Exploit.create(job=job, cs=cs, blob="exploit", pov_type='type1',
                                 c_code="c_code")

        assert_is_none(PovTestResult.best_against_cs_fielding(csf1))

        pov1 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    num_success=2)
        assert_equals(pov1, PovTestResult.best_against_cs_fielding(csf1))
        assert_is_none(PovTestResult.best_against_cs_fielding(csf2))

        pov2 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=3)
        assert_equals(pov2, PovTestResult.best_against_cs_fielding(csf1))
        assert_is_none(PovTestResult.best_against_cs_fielding(csf2))

        pov3 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=1)
        assert_equals(pov2, PovTestResult.best_against_cs_fielding(csf1))
        assert_is_none(PovTestResult.best_against_cs_fielding(csf2))

        pov4 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=4)
        pov5 = PovTestResult.create(exploit=exploit,
                                    cs_fielding=csf2,
                                    ids_fielding=idsrf1,
                                    num_success=8)
        assert_equals(pov4, PovTestResult.best_against_cs_fielding(csf1))
        assert_equals(pov5, PovTestResult.best_against_cs_fielding(csf2))

    def test_best_against_cs(self):
        team = Team.create(name=Team.OUR_NAME)
        cs1 = ChallengeSet.create(name="foo")
        cs2 = ChallengeSet.create(name="foo2")

        r1 = Round.create(num=1)
        ids1 = IDSRule.create(cs=cs1, rules="ids1", sha256="sum1")
        idsrf1 = IDSRuleFielding.create(cs=cs1, ids_rule=ids1, team=team, available_round=r1)

        cbn1 = ChallengeBinaryNode.create(name="foo_3", cs=cs1, sha256="sum3")
        csf1 = ChallengeSetFielding.create(cs=cs1, cbns=[cbn1], team=team, available_round=r1)
        job1 = AFLJob.create(cbn=cbn1, cs=cs1)
        exploit1 = Exploit.create(job=job1, cs=cs1, blob="exploit", pov_type='type1',
                                  c_code="c_code")

        r2 = Round.create(num=2)
        cbn2 = ChallengeBinaryNode.create(name="foo_3", cs=cs2, sha256="sum4")
        csf2 = ChallengeSetFielding.create(cs=cs2, cbns=[cbn2], team=team, available_round=r2)

        job2 = AFLJob.create(cbn=cbn1, cs=cs2)
        exploit2 = Exploit.create(job=job2, cs=cs2, blob="exploit", pov_type='type1',
                                  c_code="c_code")

        assert_is_none(PovTestResult.best_against_cs(cs1))

        pov1 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    num_success=2)
        assert_equals(pov1, PovTestResult.best_against_cs(cs1))

        pov2 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=3)
        assert_equals(pov2, PovTestResult.best_against_cs(cs1))
        assert_is_none(PovTestResult.best_against_cs(cs2))

        pov3 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=1)
        assert_equals(pov2, PovTestResult.best_against_cs(cs1))
        assert_is_none(PovTestResult.best_against_cs(cs2))

        pov4 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=4)
        pov5 = PovTestResult.create(exploit=exploit2,
                                    cs_fielding=csf2,
                                    ids_fielding=idsrf1,
                                    num_success=8)
        assert_equals(pov4, PovTestResult.best_against_cs(cs1))
        assert_equals(pov5, PovTestResult.best_against_cs(cs2))

    def test_exploit_test_results(self):
        team = Team.create(name=Team.OUR_NAME)
        cs1 = ChallengeSet.create(name="foo")
        cs2 = ChallengeSet.create(name="foo2")

        r1 = Round.create(num=1)
        ids1 = IDSRule.create(cs=cs1, rules="ids1", sha256="sum1")
        idsrf1 = IDSRuleFielding.create(cs=cs1, ids_rule=ids1, team=team, available_round=r1)

        cbn1 = ChallengeBinaryNode.create(name="foo_3", cs=cs1, sha256="sum3")
        csf1 = ChallengeSetFielding.create(cs=cs1, cbns=[cbn1], team=team, available_round=r1)
        job1 = AFLJob.create(cbn=cbn1, cs=cs1)
        exploit1 = Exploit.create(job=job1, cs=cs1, blob="exploit", pov_type='type1',
                                  c_code="c_code")

        r2 = Round.create(num=2)
        cbn2 = ChallengeBinaryNode.create(name="foo_3", cs=cs2, sha256="sum4")
        csf2 = ChallengeSetFielding.create(cs=cs2, cbns=[cbn2], team=team, available_round=r2)

        job2 = AFLJob.create(cbn=cbn1, cs=cs2)
        exploit2 = Exploit.create(job=job2, cs=cs2, blob="exploit", pov_type='type1',
                                  c_code="c_code")

        assert_is_none(PovTestResult.best_exploit_test_results(exploit1, csf1, None))
        assert_is_none(PovTestResult.best_exploit_test_results(exploit1, csf1, idsrf1))

        pov1 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    num_success=2)
        assert_equals(pov1, PovTestResult.best_exploit_test_results(exploit1, csf1, None))
        assert_is_none(PovTestResult.best_exploit_test_results(exploit1, csf1, idsrf1))

        pov2 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=3)
        assert_equals(pov1, PovTestResult.best_exploit_test_results(exploit1, csf1, None))
        assert_equals(pov2, PovTestResult.best_exploit_test_results(exploit1, csf1, idsrf1))

        pov3 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=1)
        assert_equals(pov1, PovTestResult.best_exploit_test_results(exploit1, csf1, None))
        assert_equals(pov2, PovTestResult.best_exploit_test_results(exploit1, csf1, idsrf1))

        pov4 = PovTestResult.create(exploit=exploit1,
                                    cs_fielding=csf1,
                                    ids_fielding=idsrf1,
                                    num_success=4)
        pov5 = PovTestResult.create(exploit=exploit2,
                                    cs_fielding=csf2,
                                    ids_fielding=idsrf1,
                                    num_success=8)
        assert_equals(pov4, PovTestResult.best_exploit_test_results(exploit1, csf1, idsrf1))
        assert_equals(pov5, PovTestResult.best_exploit_test_results(exploit2, csf2, idsrf1))
