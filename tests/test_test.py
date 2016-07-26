#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, DrillerJob, ChallengeBinaryNode, ChallengeSet, Job
import farnsworth.models    # to avoid collisions between Test and nosetests

NOW = datetime.now()


class TestTest:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_save_automatically_calculates_sha256(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create()
        test = farnsworth.models.Test(cs=cs, job=job, blob="a blob")
        assert_is_none(test.sha256)

        test.save()
        assert_equals(test.sha256, "bbffdf5ecaf101e014fa03c8d0b1996554bac10f")

        test = farnsworth.models.Test(cs=cs, job=job, blob="a blob", sha256="sum")
        test.save()
        assert_equals(test.sha256, "sum")

        test = farnsworth.models.Test.create(cs=cs, job=job, blob="another blob")
        assert_is_not_none(test.sha256)

    def test_cs_sha256_uniqueness(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create()
        test = farnsworth.models.Test.create(cs=cs, job=job, blob="a blob")

        assert_raises(farnsworth.models.Test.create, cs=cs, job=job, blob="a blob")

    def test_cs_sha256_uniqueness_across_cses(self):
        cs1 = ChallengeSet.create(name="foo1")
        cs2 = ChallengeSet.create(name="foo2")
        job1 = AFLJob.create()
        job2 = AFLJob.create()
        test1 = farnsworth.models.Test.create(cs=cs1, job=job1, blob="a blob")
        test2 = farnsworth.models.Test.create(cs=cs2, job=job2, blob="a blob")

    def test_get_or_create(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create()

        test, created = farnsworth.models.Test.get_or_create(cs=cs, job=job, blob="a blob")
        assert_true(created)
        test, created = farnsworth.models.Test.get_or_create(cs=cs, job=job, blob="a blob")
        assert_false(created)
        # because we're opening another transaction in create_or_get()
        # rollback doesn't work. clean everything in a transaction
        with ChallengeSet._meta.database.atomic():
            test.delete_instance()
            job.delete_instance()
            cs.delete_instance()

    def test_cbn_association(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create(cs=cs)
        test1 = farnsworth.models.Test.create(cs=cs, job=job, blob="testicolo sn")
        test2 = farnsworth.models.Test.create(cs=cs, job=job, blob="testicolo dx")
        assert_equals(len(cs.tests), 2)
        assert_in(test1, cs.tests)
        assert_in(test2, cs.tests)

    def test_cqe_pov_xml(self):
        cs = ChallengeSet.create(name="foo")
        job = AFLJob.create(cs=cs)
        test = farnsworth.models.Test.create(cs=cs, job=job, blob="XXX")
        test_xml = '''<?xml version="1.0" standalone="no" ?>
                        <!DOCTYPE pov SYSTEM "/usr/share/cgc-docs/replay.dtd">
                     <pov><cbid>{cbid}</cbid><replay><write><data>{data}</data></write></replay></pov>'''
        assert_equals(test.to_cqe_pov_xml(), test_xml.format(cbid=test.cs.id, data='XXX'))

    def test_unsynced_testcases(self):
        cs1 = ChallengeSet.create(name="foo")
        cs2 = ChallengeSet.create(name="foo")
        job1 = AFLJob.create(cs=cs1)
        job2 = AFLJob.create(cs=cs2)
        job3 = DrillerJob.create(cs=cs2)

        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 0)

        test1 = farnsworth.models.Test.create(cs=cs1, job=job1, blob="XXX1")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 1)

        test2 = farnsworth.models.Test.create(cs=cs2, job=job2, blob="XXX2")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 2)

        unsynced_cs1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                              .join(Job).where(Job.cs == cs1)
        assert_equal(len(unsynced_cs1), 1)

        test3 = farnsworth.models.Test.create(cs=cs1, job=job3, blob="XXX3")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 3)
        unsynced_cs2 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                              .join(Job).where(Job.cs == cs2)
        assert_equal(len(unsynced_cs2), 2)

        unsynced_cs2_job2 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                                   .join(Job).where((Job.cs == cs2) \
                                                                    & (job2.id != Job.id))
        assert_equal(len(unsynced_cs2_job2), 1)
