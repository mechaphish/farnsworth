from nose.tools import *
from datetime import datetime

from . import support
from farnsworth import PatcherexJob, AFLJob, ChallengeBinaryNode

class TestPatcherexJob:
    def setup(self):
        support.truncate_tables()

    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        job = PatcherexJob(cbn=cbn)
        assert_false(PatcherexJob.queued(job))

        useless_job = AFLJob(cbn=cbn)
        assert_false(PatcherexJob.queued(job))

        job.save()
        assert_true(PatcherexJob.queued(job))

        job.completed_at = datetime.now()
        job.save()
        assert_false(PatcherexJob.queued(job))