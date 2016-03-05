from nose.tools import *
from datetime import datetime

from . import support
from farnsworth import DrillerJob, ChallengeBinaryNode, AFLJob
import farnsworth               # to avoid collisions between Test and nosetests

class TestDrillerJob:
    def setup(self):
        support.truncate_tables()

    def test_input_test(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        generating_job = AFLJob.create(cbn=cbn)
        test = farnsworth.Test.create(job=generating_job, cbn=cbn, blob="ciao")
        job = DrillerJob(cbn=cbn, payload={'test_id': test.id})
        assert_equal(str(job.input_test.blob), "ciao")
        # it caches result between different requests
        assert_false(job.input_test.drilled)
        job.input_test.drilled = True
        job.input_test.save()
        assert_true(job.input_test.drilled)

    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        generating_job = AFLJob.create(cbn=cbn)
        test = farnsworth.Test.create(job=generating_job, cbn=cbn)
        job = DrillerJob(cbn=cbn, payload={'test_id': test.id})
        assert_false(DrillerJob.queued(job))

        job2 = DrillerJob.create(cbn=cbn, payload={'test_id': 'foo'})
        assert_false(DrillerJob.queued(job))

        job.save()
        assert_true(DrillerJob.queued(job))
