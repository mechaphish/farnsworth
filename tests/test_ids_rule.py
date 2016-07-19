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
        r0 = Round.create(num=0)
        r1 = Round.create(num=1)
        Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        ids = IDSRule.create(cs=cs, rules="aaa", sha256="bbb")

        assert_equals(len(ids.fieldings), 0)

        ids.submit()
        assert_equals(len(ids.fieldings), 1)
        assert_equals(ids.fieldings.get().team, Team.get_our())
        assert_equals(ids.fieldings.get().submission_round, Round.current_round())

        fielding = ids.submit(r0)
        assert_equals(len(ids.fieldings), 2)
        assert_equals(fielding.submission_round, r0)

    def test_generate_hash_on_create_and_save_if_missing(self):
        cs = ChallengeSet.create(name="foo")

        ids_create = IDSRule.create(cs=cs, rules="aaa")
        assert_equals(ids_create.sha256, "9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0")

        ids_save = IDSRule(cs=cs, rules="bbb")
        ids_save.save()
        assert_equals(ids_save.sha256, "3e744b9dc39389baf0c5a0660589b8402f3dbb49b89b3e75f2c9355852a3c677")

        ids_set = IDSRule.create(cs=cs, rules="ccc", sha256="ddd")
        assert_equals(ids_set.sha256, "ddd")

    def test_get_by_sha256_or_create(self):
        cs = ChallengeSet.create(name="foo")

        assert_equals(len(IDSRule.all()), 0)
        ids1 = IDSRule.get_by_sha256_or_create(rules="aaa", cs=cs)
        ids2 = IDSRule.get_by_sha256_or_create(rules="aaa", cs=cs)
        assert_equals(ids1, ids2)
        assert_equals(len(IDSRule.all()), 1)
