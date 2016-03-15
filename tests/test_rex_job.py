from nose.tools import *
from datetime import datetime

from . import support
from farnsworth import RexJob, AFLJob, ChallengeBinaryNode, Crash

class TestRexJob:
    def setup(self):
        support.truncate_tables()

    def test_queued(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        generating_job = AFLJob.create(cbn=cbn)
        crash = Crash.create(job=generating_job, cbn=cbn)
        job = RexJob(cbn=cbn, payload={'crash_id': crash.id})
        assert_false(RexJob.queued(job))

        useless_job = AFLJob(cbn=cbn, payload={'crash_id': crash.id})
        assert_false(RexJob.queued(job))

        job2 = RexJob.create(cbn=cbn, payload={'crash_id': 'foo'})
        assert_false(RexJob.queued(job))

        job.save()
        assert_true(RexJob.queued(job))
