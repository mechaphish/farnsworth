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
                               IDSRule,
                               Round)

class TestCSSubmissionCable:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_get_or_create(self):
        r = Round.create(num=0)
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo1", cs=cs, blob="aaa1")
        cbn2 = ChallengeBinaryNode.create(name="foo1", cs=cs, blob="aaa2")
        ids = IDSRule.create(cs=cs, rules="aaa", sha256="sum")

        cbl1, crtd1 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1], round=r)
        assert_true(crtd1)

        cbl2, crtd2 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1], round=r)
        assert_false(crtd2)
        assert_equals(cbl1.id, cbl2.id)

        cbl3, crtd3 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1, cbn2], round=r)
        assert_true(crtd3)

        cbl4, crtd4 = CSSubmissionCable.get_or_create(cs=cs, ids=ids, cbns=[cbn1, cbn2], round=r)
        assert_false(crtd4)
        assert_equals(cbl3.id, cbl4.id)
