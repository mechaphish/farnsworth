from nose.tools import *
import time
import os
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, IDSRule

class TestIDSRule:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_submit(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        ids = IDSRule.create(cbn = cbn, rules = "aaa")

        assert_is_none(ids.submitted_at)
        ids.submit()
        assert_is_instance(ids.submitted_at, datetime)

    def test_unsubmitted(self):
        cbn = ChallengeBinaryNode.create(name = "foo", cs_id = "foo")
        ids1 = IDSRule.create(cbn = cbn, rules = "aaa")
        ids2 = IDSRule.create(cbn = cbn, rules = "bbb", submitted_at = datetime.now())

        assert_equals(len(IDSRule.unsubmitted()), 1)
        assert_in(ids1, IDSRule.unsubmitted())
