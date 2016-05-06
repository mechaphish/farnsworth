from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode
from farnsworth.models.job import *

class TestJob:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_to_job_type(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        afl_job = AFLJob.create(cbn=cbn)
        driller_job = DrillerJob.create(cbn=cbn)
        rex_job = RexJob.create(cbn=cbn)
        patcherex_job = PatcherexJob.create(cbn=cbn)
        tester_job = TesterJob.create(cbn=cbn)

        jobs = Job.select().order_by(Job.id.asc())
        for job in jobs:
            print "{0.id}-{0.__class__}".format(job)
        assert_is_instance(to_job_type(jobs[0]), AFLJob)
        assert_is_instance(to_job_type(jobs[1]), DrillerJob)
        assert_is_instance(to_job_type(jobs[2]), RexJob)
        assert_is_instance(to_job_type(jobs[3]), PatcherexJob)
        assert_is_instance(to_job_type(jobs[4]), TesterJob)
