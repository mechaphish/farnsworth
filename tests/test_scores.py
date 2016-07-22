#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from . import setup_each, teardown_each
from farnsworth.models import (
    PollFeedback, ChallengeSet, Round, Team, ChallengeSetFielding, ChallengeBinaryNode
)

BLOB = "cb scores"

#pylint:disable=no-self-use

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

        csf_orig = ChallengeSetFielding.create(
            cs=cs, cbns=[cbn1], team=team, available_round=ra, submission_round=ra,
            poll_feedback = PollFeedback.create(
                cs=cs,
                round_id=ra.id,
                success=1.0,
                timeout=0,
                connect=0,
                function=0,
                time_overhead=0.0,
                memory_overhead=0.0,
            )
        )

        csf_patched = ChallengeSetFielding.create(
            cs=cs, cbns=[cbn2], team=team, available_round=rb,
            poll_feedback = PollFeedback.create(
                cs=cs,
                round_id=ra.id,
                success=1.0,
                timeout=0,
                connect=0,
                function=0,
                time_overhead=0.0,
                memory_overhead=0.0,
            )
        )

        assert cbn2.min_cb_score < 1.

    def test_cbn_to_polls(self):
        r3 = Round.create(num=3)
        r4 = Round.create(num=4)
        r5 = Round.create(num=5)
        cs = ChallengeSet.create(name="foo2")
        team = Team.get_our()
        cbn1 = ChallengeBinaryNode.create(name="foo_2", cs=cs, sha256="sum2", blob="asdf")
        csf3 = ChallengeSetFielding.create(
            cs=cs, cbns=[cbn1], team=team, available_round=r3, submission_round=r3,
            poll_feedback = PollFeedback.create(
                cs=cs,
                round_id=r3.id,
                success=0.0,
                timeout=0,
                connect=0,
                function=0,
                time_overhead=0.0,
                memory_overhead=0.0,
            )
        )
        csf4 = ChallengeSetFielding.create(
            cs=cs, cbns=[cbn1], team=team, available_round=r4,
            poll_feedback = PollFeedback.create(
                cs=cs,
                round_id=r4.id,
                success=0.99,
                timeout=0,
                connect=0,
                function=0,
                time_overhead=0.0,
                memory_overhead=0.0,
            )
        )
        csf5 = ChallengeSetFielding.create(
            cs=cs, cbns=[cbn1], team=team, available_round=r5,
            # some variance
            poll_feedback = PollFeedback.create(
                cs=cs,
                round_id=r5.id,
                success=0.99,
                timeout=0,
                connect=0,
                function=0,
                time_overhead=0.0,
                memory_overhead=0.2,
            )
        )

        assert len(cbn1.poll_feedbacks) == 2
        assert cbn1.avg_cb_score == (0.9609803444828162 + 0.6830134553650711)/2
        assert cbn1.min_cb_score == 0.6830134553650711

    def test_poll_feedback(self):
        r0 = Round.create(num=0)
        cs = ChallengeSet.create(name="foo")
        team = Team.get_our()
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, sha256="sum1", blob="asdf")
        csf = ChallengeSetFielding.create(cs=cs, cbns=[cbn1], team=team, available_round=r0)

        # check full score
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=1.0,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.0,
            memory_overhead=0.0,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.cqe_performance_score == 1.0
        assert p.cqe_functionality_score == 1.0
        assert p.availability == 1.0
        assert p.cb_score == 1.0

        # check minimum overhead
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=1.0,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.0,
            memory_overhead=0.09,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.memory_overhead == 0.09
        assert p.availability == 1.0
        assert p.cb_score == 1.0

        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=1.0,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.03,
            memory_overhead=0.03,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.availability == 1.0
        assert p.cb_score == 1.0


        # check failed polls
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=0.99,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.03,
            memory_overhead=0.03,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.availability == 0.9609803444828162
        assert p.cb_score == 0.9609803444828162

        # check more failures
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=0.97,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.0,
            memory_overhead=0.0,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.availability == 0.8884870479156888
        assert p.cb_score == 0.8884870479156888

        # check high failures
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=0.01,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.0,
            memory_overhead=0.0,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.availability == 0.00381
        assert p.cb_score == 0.00381

        # check high overhead
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=0.99,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=0.10,
            memory_overhead=0.20,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.availability == 0.6830134553650711
        assert p.cb_score == 0.6830134553650711

        # check full overhead
        p = PollFeedback.create(
            cs=cs,
            round_id=r0.id,
            success=0.99,
            timeout=0,
            connect=0,
            function=0,
            time_overhead=1.00,
            memory_overhead=0.20,
        )
        csf.poll_feedback = p
        csf.save()

        assert p.availability == 0
        assert p.cb_score == 0
