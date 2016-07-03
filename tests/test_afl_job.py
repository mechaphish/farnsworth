from nose.tools import *
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, RexJob, ChallengeBinaryNode

class TestAFLJob:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_added_completed(self):
        cbn = ChallengeBinaryNode.create(name="foo", cs_id="foo")
        job = AFLJob(cbn=cbn)
        assert_raises(AFLJob.DoesNotExist, AFLJob.get, cbn=cbn)

        useless_job = RexJob(cbn=cbn)
        assert_raises(AFLJob.DoesNotExist, AFLJob.get, cbn=cbn)

        job.save()
        job = AFLJob.get(cbn=cbn)

        job.completed_at = datetime.now()
        job.save()
        assert_raises(AFLJob.DoesNotExist, AFLJob.get, cbn=cbn, completed_at=None)
