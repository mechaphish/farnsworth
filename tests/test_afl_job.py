from nose.tools import *
from datetime import datetime

from . import support
from farnsworth import AFLJob, ChallengeBinaryNode

class TestAFLJob:
    def setup(self):
        support.truncate_tables()

    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        job = AFLJob(cbn=cbn)
        assert_false(AFLJob.queued(job))

        job.save()
        assert_true(AFLJob.queued(job))

        job.completed_at = datetime.now()
        job.save()
        assert_false(AFLJob.queued(job))
