#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import Round

class TestRound:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_current_round(self):
        assert_equals(Round.current_round(), None)

        now = datetime.datetime.now()
        Round.create(num=0, ends_at=(now + datetime.timedelta(seconds=15)))
        Round.create(num=1, ends_at=(now + datetime.timedelta(seconds=25)))
        Round.create(num=2, ends_at=(now + datetime.timedelta(seconds=35)))
        assert_equals(Round.current_round().num, 2)

    def test_at_timestamp(self):
        now = datetime.datetime.now()
        round0 = Round.create(num=0, created_at=(now + datetime.timedelta(seconds=10)),
                              ends_at=(now + datetime.timedelta(seconds=15)))
        round1 = Round.create(num=1, created_at=(now + datetime.timedelta(seconds=20)),
                              ends_at=(now + datetime.timedelta(seconds=25)))
        round2 = Round.create(num=2, created_at=(now + datetime.timedelta(seconds=30)),
                              ends_at=(now + datetime.timedelta(seconds=35)))

        assert_is_none(Round.at_timestamp(now + datetime.timedelta(seconds=5)))
        assert_equals(Round.at_timestamp(now + datetime.timedelta(seconds=15)).num, 0)
        assert_equals(Round.at_timestamp(now + datetime.timedelta(seconds=25)).num, 1)
        assert_equals(Round.at_timestamp(now + datetime.timedelta(seconds=35)).num, 2)
