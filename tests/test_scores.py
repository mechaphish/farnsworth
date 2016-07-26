#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models.challenge_binary_node import ChallengeBinaryNode
from farnsworth.models.challenge_set_fielding import ChallengeSetFielding
from farnsworth.models.challenge_set import ChallengeSet
from farnsworth.models.patch_score import PatchScore
from farnsworth.models.patch_type import PatchType
from farnsworth.models.poll_feedback import PollFeedback
from farnsworth.models.round import Round
from farnsworth.models.team import Team

BLOB = "cb scores"

# pylint:disable=no-self-use

class TestScores(object):
    def setup(self):
        setup_each()
        Team.create(name=Team.OUR_NAME)

    def teardown(self):
        teardown_each()

    def test_size_overhead(self):
        ra = Round.create(num=6)
        rb = Round.create(num=7)
        cs = ChallengeSet.create(name="foo3")
        team = Team.get_our()
        cbn1 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum3", blob="asdf")
        cbn2 = ChallengeBinaryNode.create(name="foo_3a", cs=cs, sha256="sum4", blob="asdf11")

        pf = PollFeedback.create(cs=cs, round=ra, success=1.0, timeout=0, connect=0,
                                 function=0, time_overhead=0.0, memory_overhead=0.0)
        csf_orig = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=ra,
                                               submission_round=ra, poll_feedback=pf)

        pf = PollFeedback.create(cs=cs, round=ra, success=1.0, timeout=0, connect=0,
                                 function=0, time_overhead=0.0, memory_overhead=0.0)
        csf_patched = ChallengeSetFielding.create(cs=cs, cbns=[cbn2], team=team,
                                                  available_round=rb, poll_feedback=pf)

        assert_less(cbn2.min_cb_score, 1.0)

    def test_cbn_to_polls(self):
        r3 = Round.create(num=3)
        r4 = Round.create(num=4)
        r5 = Round.create(num=5)
        cs = ChallengeSet.create(name="foo2")
        team = Team.get_our()
        cbn1 = ChallengeBinaryNode.create(name="foo_2", cs=cs, sha256="sum2", blob="asdf")

        assert_is_none(cbn1.avg_cb_score)
        assert_is_none(cbn1.min_cb_score)

        pf = PollFeedback.create(cs=cs, round=r3, success=0.0, timeout=0, connect=0,
                                 function=0, time_overhead=0.0, memory_overhead=0.0)
        csf3 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r3,
                                           submission_round=r3, poll_feedback=pf)

        pf = PollFeedback.create(cs=cs, round=r4, success=0.99, timeout=0,
                                                connect=0, function=0, time_overhead=0.0,
                                                memory_overhead=0.0)
        csf4 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r4,
                                           poll_feedback=pf)

        pf = PollFeedback.create(cs=cs, round=r5, success=0.99, timeout=0, connect=0,
                                 function=0, time_overhead=0.0, memory_overhead=0.2)
        csf5 = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r5,
                                           poll_feedback=pf)

        assert_equal(len(cbn1.poll_feedbacks), 2)
        assert_almost_equal(cbn1.avg_cb_score, ((0.9609803444828162 + 0.6830134553650711)/2))
        assert_almost_equal(cbn1.min_cb_score, 0.6830134553650711)

    def test_poll_feedback(self):
        r0 = Round.create(num=0)
        cs = ChallengeSet.create(name="foo")
        team = Team.get_our()
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, sha256="sum1", blob="asdf")
        csf = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r0)

        # Check full score
        p = PollFeedback.create(cs=cs, round=r0, success=1.0, timeout=0, connect=0,
                                function=0, time_overhead=0.0, memory_overhead=0.0)
        csf.poll_feedback = p
        csf.save()

        assert_equal(p.cqe_performance_score, 1)
        assert_equal(p.cqe_functionality_score, 1)
        assert_equal(p.availability, 1)
        assert_equal(p.cb_score, 1)

        # Check minimum overhead
        p = PollFeedback.create(cs=cs, round=r0, success=1.0, timeout=0, connect=0,
                                function=0, time_overhead=0.0, memory_overhead=0.09)
        csf.poll_feedback = p
        csf.save()

        assert_equal(p.memory_overhead, 0.09)
        assert_equal(p.availability, 1)
        assert_equal(p.cb_score, 1)

        p = PollFeedback.create(cs=cs, round=r0, success=1.0, timeout=0, connect=0,
                                function=0, time_overhead=0.03, memory_overhead=0.03)
        csf.poll_feedback = p
        csf.save()

        assert_equal(p.availability, 1)
        assert_equal(p.cb_score, 1)

        # Check failed polls
        p = PollFeedback.create(cs=cs, round=r0, success=0.99, timeout=0, connect=0,
                                function=0, time_overhead=0.03, memory_overhead=0.03,)
        csf.poll_feedback = p
        csf.save()

        assert_almost_equal(p.availability, 0.9609803444828162)
        assert_almost_equal(p.cb_score, 0.9609803444828162)

        # Check more failures
        p = PollFeedback.create(cs=cs, round=r0, success=0.97, timeout=0, connect=0,
                                function=0, time_overhead=0.0, memory_overhead=0.0)
        csf.poll_feedback = p
        csf.save()

        assert_almost_equal(p.availability, 0.8884870479156888)
        assert_almost_equal(p.cb_score, 0.8884870479156888)

        # Check high failures
        p = PollFeedback.create(cs=cs, round=r0, success=0.01, timeout=0, connect=0,
                                function=0, time_overhead=0.0, memory_overhead=0.0)
        csf.poll_feedback = p
        csf.save()

        assert_equal(p.availability, 0.00381)
        assert_equal(p.cb_score, 0.00381)

        # Check high overhead
        p = PollFeedback.create(cs=cs, round=r0, success=0.99, timeout=0, connect=0,
                                function=0, time_overhead=0.10, memory_overhead=0.20)
        csf.poll_feedback = p
        csf.save()

        assert_almost_equal(p.availability, 0.6830134553650711)
        assert_almost_equal(p.cb_score, 0.6830134553650711)

        # Check full overhead
        p = PollFeedback.create(cs=cs, round=r0, success=0.99, timeout=0, connect=0,
                                function=0, time_overhead=1.00, memory_overhead=0.20)
        csf.poll_feedback = p
        csf.save()

        assert_equal(p.availability, 0)
        assert_equal(p.cb_score, 0)

    def test_esimated_cb_score(self):
        r6 = Round.create(num=6)
        team = Team.get_our()

        cs = ChallengeSet.create(name="foo3")
        cbn1 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum3", blob="asdf")
        pt = PatchType.create(name="patch1", functionality_risk=0.0, exploitability=0.2)

        # PatchType exists, but no patched binary
        assert_is_none(cbn1.estimated_cb_score)

        # Patched
        cbn2 = ChallengeBinaryNode.create(name="foo_3", cs=cs, sha256="sum4", blob="asdf",
                                          patch_type=pt)

        pf = PollFeedback.create(cs=cs, round=r6, success=1.0, timeout=0, connect=0,
                                 function=0, time_overhead=0.0, memory_overhead=0.0)

        perf_score = {'score': {'rep': {'task_clock': 4,
                                        'rss': 3,
                                        'flt': 1,
                                        'file_size': 5},
                                'ref': {'task_clock': 4,
                                        'rss': 3,
                                        'flt': 2,
                                        'file_size': 6}}}
        ps = PatchScore.create(cs=cs, round=r6, num_polls=1, perf_score=perf_score, patch_type=pt)
        csf_orig = ChallengeSetFielding.create(cs=cs, cbns=[cbn2], team=team, available_round=r6,
                                               submission_round=r6, poll_feedback=pf)
        assert_almost_equals(cbn2.estimated_cb_score, 1.8)
