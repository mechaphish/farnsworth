from nose.tools import *
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, Job

class TestAFLJob:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_save(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        job = Job(cbn=cbn, worker='basemodel')

        updated_at = job.updated_at
        job.worker = '#aftersave'
        job.save()
        assert_greater(job.updated_at, updated_at)
