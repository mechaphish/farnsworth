from nose.tools import *
import time
import os
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import ChallengeSet, IDSRule

class TestIDSRule:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_submit(self):
        cs = ChallengeSet.create(name = "foo")
        ids = IDSRule.create(cs = cs, rules = "aaa")

        assert_is_none(ids.submitted_at)
        ids.submit()
        assert_is_instance(ids.submitted_at, datetime)
