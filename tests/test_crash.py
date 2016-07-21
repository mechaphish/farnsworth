#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, ChallengeSet, Crash


class TestCrash:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_save_and_create_automatically_calculates_sha256(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create()
        crash = Crash(cs=cs, job=job, blob="a blob")
        assert_is_none(crash.sha256)

        crash.save()
        assert_equals(crash.sha256, "bbffdf5ecaf101e014fa03c8d0b1996554bac10f")

        crash = Crash(cs=cs, job=job, blob="a blob", sha256="sum")
        crash.save()
        assert_equals(crash.sha256, "sum")

        crash = Crash.create(cs=cs, job=job, blob="another blob")
        assert_is_not_none(crash.sha256)

    def test_cs_sha256_uniqueness(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create()
        crash = Crash.create(cs=cs, job=job, blob="a blob")

        assert_raises(Crash.create, cs=cs, job=job, blob="a blob")

    def test_get_or_create(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create()

        crash, created = Crash.get_or_create(cs=cs, job=job, blob="a blob")
        assert_true(created)
        crash, created = Crash.get_or_create(cs=cs, job=job, blob="a blob")
        assert_false(created)
        # because we're opening another transaction in create_or_get()
        # rollback doesn't work. clean everything in a transaction
        with Crash._meta.database.atomic():
            crash.delete_instance()
            job.delete_instance()
            cs.delete_instance()
