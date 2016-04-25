from nose.tools import *
from datetime import datetime

from farnsworth.models import AFLJob, RexJob, ChallengeBinaryNode

class TestAFLJob:
    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        job = AFLJob(cbn=cbn)
        assert_false(AFLJob.queued(job))

        useless_job = RexJob.create(cbn=cbn)
        assert_false(AFLJob.queued(job))

        job.save()
        assert_true(AFLJob.queued(job))

        job.completed_at = datetime.now()
        job.save()
        assert_false(AFLJob.queued(job))
