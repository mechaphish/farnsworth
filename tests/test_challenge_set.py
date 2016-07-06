from nose.tools import *
import time
import os
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, ChallengeSet, IDSRule

class TestChallengeSet:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_unsubmitted_ids_rules(self):
        cs = ChallengeSet.create(name = "foo")
        ids1 = IDSRule.create(cs = cs, rules = "aaa")
        ids2 = IDSRule.create(cs = cs, rules = "bbb", submitted_at = datetime.now())

        assert_equals(len(cs.unsubmitted_ids_rules), 1)
        assert_in(ids1, cs.unsubmitted_ids_rules)

    def test_cbns_by_patch_type(self):
        cs = ChallengeSet.create(name = "foo")
        cbn = ChallengeBinaryNode.create(name = "foo", cs = cs)
        cbn1 = ChallengeBinaryNode.create(name = "foo1", cs = cs, patch_type="patch0")
        cbn2 = ChallengeBinaryNode.create(name = "foo2", cs = cs, patch_type="patch0")
        cbn3 = ChallengeBinaryNode.create(name = "foo3", cs = cs, patch_type="patch1")

        assert_equals(['original', 'patch0', 'patch1'], sorted(cs.cbns_by_patch_type().keys()))

        assert_equals(cs.cbns_by_patch_type()['original'], [cbn])
        assert_equals([cbn1, cbn2], cs.cbns_by_patch_type()['patch0'])
        assert_equals([cbn3], cs.cbns_by_patch_type()['patch1'])
