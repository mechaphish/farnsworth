#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, ChallengeSet, Job

class TestBaseModel:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_save(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs)
        job = Job(cbn=cbn, worker='basemodel')

        updated_at = job.updated_at
        job.worker = '#aftersave'
        job.save()
        assert_greater(job.updated_at, updated_at)

    def test_get_or_create(self):
        assert_equals(len(ChallengeSet.select()), 0)
        cs1, _ = ChallengeSet.get_or_create(name="foo")
        cs2, _ = ChallengeSet.get_or_create(name="foo")
        cs3, _ = ChallengeSet.get_or_create(name="bar")

        assert_equals(len(ChallengeSet.select()), 2)
        assert_equals(cs2.id, cs1.id)
        assert_not_equals(cs3.id, cs1.id)

        ChallengeBinaryNode.delete().execute()
        ChallengeSet.delete().execute()
        ChallengeSet._meta.database.commit()

    def test_all(self):
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo", cs=cs)
        cbn2 = ChallengeBinaryNode.create(name="bar", cs=cs)

        assert_equals(len(ChallengeBinaryNode.all()), 2)
        assert_equals(ChallengeBinaryNode.all()[0], cbn1)
        assert_equals(ChallengeBinaryNode.all()[1], cbn2)
