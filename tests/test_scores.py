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

    def teardown(self):
        teardown_each()

    def test_poll_feedback(self):
        r0 = Round.create(num=0)
        cs = ChallengeSet.create(name="foo")
        team = Team.create(name=Team.OUR_NAME)
        cbn1 = ChallengeBinaryNode.create(name="foo_1", cs=cs, sha256="sum1")
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
            size_overhead=0.0,
        )

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
            size_overhead=0.0,
        )

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
            size_overhead=0.03,
        )

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
            size_overhead=0.03,
        )

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
            size_overhead=0.0,
        )

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
            size_overhead=0.0,
        )

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
            size_overhead=0.10,
        )

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
            size_overhead=0.10,
        )

        assert p.availability == 0
        assert p.cb_score == 0
