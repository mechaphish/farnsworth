from nose.tools import *

import farnsworth.test_support
from farnsworth.models import ChallengeBinaryNode, AFLJob
import farnsworth.models # to avoid collisions between Test and nosetests

class TestTest:
    def setup(self):
        farnsworth.test_support.truncate_tables()

    def test_cbn_association(self):
        cbn = ChallengeBinaryNode.create(name="foo", cs_id="foo")
        job = AFLJob.create(cbn=cbn)
        test1 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="testicolo sn")
        test2 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="testicolo dx")
        assert_equals(len(cbn.tests), 2)
        assert_in(test1, cbn.tests)
        assert_in(test2, cbn.tests)
