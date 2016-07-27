#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import Round

NOW = datetime.now()


class TestRound:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_prev_round(self):
        assert_equals(Round.prev_round(), None)
        Round.create(num=0)
        assert_equals(Round.prev_round(), None)
        r1 = Round.create(num=1)
        Round.create(num=2)
        assert_equals(Round.prev_round(), r1)

    def test_prev_round_on_new_game(self):
        Round.create(num=99)
        assert_equals(Round.prev_round(), None)
        r0 = Round.create(num=0)
        assert_equals(Round.prev_round(), None)
        Round.create(num=1)
        assert_equals(Round.prev_round(), r0)

    def test_current_round(self):
        assert_equals(Round.current_round(), None)
        Round.create(num=0)
        Round.create(num=1)
        Round.create(num=2)
        assert_equals(Round.current_round().num, 2)

    def test_at_timestamp(self):
        round0 = Round.create(num=0, created_at=(NOW + timedelta(seconds=10)))
        round1 = Round.create(num=1, created_at=(NOW + timedelta(seconds=20)))
        round2 = Round.create(num=2, created_at=(NOW + timedelta(seconds=30)))

        assert_is_none(Round.at_timestamp(NOW + timedelta(seconds=5)))
        assert_equals(Round.at_timestamp(NOW + timedelta(seconds=15)).num, 0)
        assert_equals(Round.at_timestamp(NOW + timedelta(seconds=25)).num, 1)
        assert_equals(Round.at_timestamp(NOW + timedelta(seconds=35)).num, 2)

    def test_ready(self):
        round0 = Round.create(num=0)
        assert_false(round0.is_ready())
        round0.ready()
        assert_true(round0.is_ready())
