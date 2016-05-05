from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode
from farnsworth.models.job import *

class TestJob:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_subclass(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        afl_job = AFLJob.create(cbn=cbn)
        driller_job = DrillerJob.create(cbn=cbn)
        rex_job = RexJob.create(cbn=cbn)
        patcherex_job = PatcherexJob.create(cbn=cbn)
        tester_job = TesterJob.create(cbn=cbn)

        jobs = Job.select().order_by(Job.id.asc())
        for j in jobs: print str(j.id) + "-" + str(j.__class__)
        assert_is_instance(jobs[0].subclass(), AFLJob)
        assert_is_instance(jobs[1].subclass(), DrillerJob)
        assert_is_instance(jobs[2].subclass(), RexJob)
        assert_is_instance(jobs[3].subclass(), PatcherexJob)
        assert_is_instance(jobs[4].subclass(), TesterJob)
