#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import time
import os

from nose.tools import *
from peewee import IntegrityError

from . import setup_each, teardown_each
from farnsworth.models import (ChallengeBinaryNode,
                               ChallengeSet,
                               CSSubmissionCable,
                               IDSRule)

class TestCSSubmissionCable:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_get_or_create(self):
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo1", cs=cs, blob="aaa1")
        cbn2 = ChallengeBinaryNode.create(name="foo1", cs=cs, blob="aaa2")
        ids = IDSRule.create(cs=cs, rules="aaa", sha256="sum")

        cable, created = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1])
        assert_true(created)

        cable2, created2 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1])
        assert_false(created2)
        assert_equals(cable.id, cable2.id)

        cable3, created3 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1, cbn2])
        assert_true(created3)

        cable4, created4 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1, cbn2])
        assert_false(created4)
        assert_equals(cable3.id, cable4.id)
