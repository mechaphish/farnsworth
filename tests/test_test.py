from nose.tools import *

from . import support
from farnsworth import ChallengeBinaryNode, AFLJob
import farnsworth               # to avoid collisions between Test and nosetests

class TestTest:
    def setup(self):
        support.truncate_tables()

    def test_cbn_association(self):
        cbn = ChallengeBinaryNode.create(name="foo", cs_id="foo")
        job = AFLJob.create(cbn=cbn)
        test1 = farnsworth.Test.create(cbn=cbn, job=job, blob="testicolo sn")
        test2 = farnsworth.Test.create(cbn=cbn, job=job, blob="testicolo dx")
        assert_equals(len(cbn.tests), 2)
        assert_in(test1, cbn.tests)
        assert_in(test2, cbn.tests)
