from nose.tools import *
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, ChallengeSet, Job

class TestBaseModel:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_save(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        job = Job(cbn=cbn, worker='basemodel')

        updated_at = job.updated_at
        job.worker = '#aftersave'
        job.save()
        assert_greater(job.updated_at, updated_at)

    def test_find_or_create(self):
        assert_equals(len(ChallengeSet.select()), 0)
        cs1 = ChallengeSet.find_or_create(name = "foo")
        cs2 = ChallengeSet.find_or_create(name = "foo")
        cs3 = ChallengeSet.find_or_create(name = "bar")

        assert_equals(len(ChallengeSet.select()), 2)
        assert_equals(cs2.id, cs1.id)
        assert_not_equals(cs3.id, cs1.id)
