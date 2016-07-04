from nose.tools import *
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import IDSJob, ChallengeSet

class TestIDSJob:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_cs(self):
        cs = ChallengeSet.create(name = "foo")
        job1 = IDSJob.create(payload={'cs_id': cs.id})
        job2 = IDSJob.create(payload={})
        assert_equals(job1.cs, cs)
        assert_is_none(job2.cs)
