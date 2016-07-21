#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, ChallengeSet, Job, Round

NOW = datetime.now()


class TestBaseModel:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_save(self):
        r1 = Round.create(num=0)
        cs = ChallengeSet.create(name="foo")
        cs.rounds = [r1]
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum")
        job = Job(cbn=cbn, worker='basemodel')

        updated_at = job.updated_at
        job.worker = '#aftersave'
        job.save()
        assert_greater(job.updated_at, updated_at)

    def test_get_or_create(self):
        assert_equals(len(ChallengeSet.select()), 0)
        r1 = Round.create(num=0)
        cs1, _ = ChallengeSet.get_or_create(name="foo")
        cs2, _ = ChallengeSet.get_or_create(name="foo")
        cs3, _ = ChallengeSet.get_or_create(name="bar")

        for cs in [cs1, cs2, cs3]:
            cs.rounds = [r1.id]

        assert_equals(len(ChallengeSet.select()), 2)
        assert_equals(cs2.id, cs1.id)
        assert_not_equals(cs3.id, cs1.id)

        cs3.delete_instance(recursive=True)
        cs2.delete_instance(recursive=True)
        cs1.delete_instance(recursive=True)
        r1.delete_instance(recursive=True)
        ChallengeSet._meta.database.commit()

    def test_all(self):
        r1 = Round.create(num=0)
        cs = ChallengeSet.create(name="foo")
        cs.rounds = [r1]
        cbn1 = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum1")
        cbn2 = ChallengeBinaryNode.create(name="bar", cs=cs, sha256="sum2")

        assert_equals(len(ChallengeBinaryNode.all()), 2)
        assert_equals(ChallengeBinaryNode.all()[0], cbn1)
        assert_equals(ChallengeBinaryNode.all()[1], cbn2)
