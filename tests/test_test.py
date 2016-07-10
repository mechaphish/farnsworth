#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, ChallengeBinaryNode, ChallengeSet, Job
import farnsworth.models    # to avoid collisions between Test and nosetests

NOW = datetime.now()


class TestTest:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_cbn_association(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, blob="blob data")
        job = AFLJob.create(cbn=cbn)
        test1 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="testicolo sn")
        test2 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="testicolo dx")
        assert_equals(len(cbn.tests), 2)
        assert_in(test1, cbn.tests)
        assert_in(test2, cbn.tests)

    def test_cqe_pov_xml(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, blob="blob data")
        job = AFLJob.create(cbn=cbn)
        test = farnsworth.models.Test.create(cbn=cbn, job=job, blob="XXX")
        test_xml = '''<?xml version="1.0" standalone="no" ?>
                        <!DOCTYPE pov SYSTEM "/usr/share/cgc-docs/replay.dtd">
                     <pov><cbid>{cbid}</cbid><replay><write><data>{data}</data></write></replay></pov>'''
        assert_equals(test.to_cqe_pov_xml(), test_xml.format(cbid=test.cbn.id, data='XXX'))

    def test_unsynced_testcases(self):
        cs1 = ChallengeSet.create(name="foo")
        cs2 = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="foo", cs=cs1, blob="blob data")
        cbn2 = ChallengeBinaryNode.create(name="bar", cs=cs2, blob="blob data")
        job1 = AFLJob.create(cbn=cbn1)
        job2 = AFLJob.create(cbn=cbn2)
        job3 = AFLJob.create(cbn=cbn1)

        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 0)

        test1 = farnsworth.models.Test.create(cbn=cbn1, job=job1, blob="XXX")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 1)

        test2 = farnsworth.models.Test.create(cbn=cbn2, job=job2, blob="XXX")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 2)

        unsynced_cbn1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                              .join(Job).where(Job.cbn == cbn1)
        assert_equal(len(unsynced_cbn1), 1)

        test3 = farnsworth.models.Test.create(cbn=cbn1, job=job3, blob="XXX")
        assert_equal(len(farnsworth.models.Test.unsynced_testcases(NOW)), 3)
        unsynced_cbn1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                              .join(Job).where(Job.cbn == cbn1)
        assert_equal(len(unsynced_cbn1), 2)

        unsynced_cbn1_job1 = farnsworth.models.Test.unsynced_testcases(NOW) \
                                                   .join(Job).where((Job.cbn == cbn1) \
                                                                    & (job1.id != Job.id))
        assert_equal(len(unsynced_cbn1_job1), 1)
