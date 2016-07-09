#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import DrillerJob, ChallengeBinaryNode, ChallengeSet, AFLJob
import farnsworth.models               # to avoid collisions between Test and nosetests


class TestDrillerJob:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_input_test(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs)
        generating_job = AFLJob.create(cbn=cbn)
        test = farnsworth.models.Test.create(job=generating_job, cbn=cbn, blob=str("ciao"))
        job = DrillerJob(cbn=cbn, payload={'test_id': test.id})

        assert_equal(str(job.input_test.blob), "ciao")
        # it caches result between different requests
        assert_false(job.input_test.drilled)

        job.input_test.drilled = True
        job.input_test.save()
        assert_true(job.input_test.drilled)
