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

        test1 = farnsworth.models.Test.create(cs=cs1, job=job1, blob="XXX")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 1)

        test2 = farnsworth.models.Test.create(cs=cs2, job=job2, blob="XXX")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 2)

        unsynced_cbn1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                              .join(Job).where(Job.cs == cs1)
        assert_equal(len(unsynced_cbn1), 1)

        test3 = farnsworth.models.Test.create(cs=cs1, job=job3, blob="XXX")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 3)
        unsynced_cbn1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                              .join(Job).where(Job.cs == cs1)
        assert_equal(len(unsynced_cbn1), 2)

        unsynced_cbn1_job1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                                   .join(Job).where((Job.cs == cs2) \
                                                                    & (job1.id != Job.id))
        assert_equal(len(unsynced_cbn1_job1), 1)
