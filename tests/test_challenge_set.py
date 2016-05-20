from nose.tools import *
import time
import os
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import ChallengeSet, IDSRule

class TestChallengeSet:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_unsubmitted_ids_rules(self):
        cs = ChallengeSet.create(name = "foo")
        ids1 = IDSRule.create(cs = cs, rules = "aaa")
        ids2 = IDSRule.create(cs = cs, rules = "bbb", submitted_at = datetime.now())

        assert_equals(len(cs.unsubmitted_ids_rules), 1)
        assert_in(ids1, cs.unsubmitted_ids_rules)
