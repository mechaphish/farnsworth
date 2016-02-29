from nose.tools import *

from . import loadenv
from farnsworth import *

class TestChallengeBinaryNode:
    def test_relationship(self):
        cbn = ChallengeBinaryNode.create(name = "test")
        job = Job.create(worker = "afl", cbn = cbn)
        assert_equals(job.cbn.id, cbn.id)
