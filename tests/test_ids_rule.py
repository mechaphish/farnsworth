#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import os
import time

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeSet, IDSRule, Round, Team


class TestIDSRule:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_submit(self):
        Round.create(num=0 ends_at=datetime.now() + timedelta(seconds=30))
        Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        ids = IDSRule.create(cs=cs, rules="aaa")

        assert_equals(len(ids.fieldings), 0)
        ids.submit()
        assert_equals(len(ids.fieldings), 1)
        assert_equals(ids.fieldings.get().team, Team.get_our())
        assert_equals(ids.fieldings.get().submission_round, Round.get_current())
