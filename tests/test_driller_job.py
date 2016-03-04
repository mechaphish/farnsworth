from nose.tools import *
from datetime import datetime

from . import support
from farnsworth import DrillerJob, ChallengeBinaryNode, Test, AFLJob

class TestDrillerJob:
    def setup(self):
        support.truncate_tables()

    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        generating_job = AFLJob.create(cbn=cbn)
        test = Test.create(job=generating_job, cbn=cbn)
        job = DrillerJob(cbn=cbn, payload={'test_id': test.id})
        assert_false(DrillerJob.queued(job))

        job2 = DrillerJob.create(cbn=cbn, payload={'test_id': 'foo'})
        assert_false(DrillerJob.queued(job))

        job.save()
        assert_true(DrillerJob.queued(job))
