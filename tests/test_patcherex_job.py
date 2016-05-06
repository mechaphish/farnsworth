from nose.tools import *
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import PatcherexJob, AFLJob, ChallengeBinaryNode

class TestPatcherexJob:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        job = PatcherexJob(cbn=cbn)
        assert_false(PatcherexJob.queued(job))

        useless_job = AFLJob(cbn=cbn)
        assert_false(PatcherexJob.queued(job))

        job.save()
        assert_true(PatcherexJob.queued(job))
