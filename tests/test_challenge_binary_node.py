from nose.tools import *

import farnsworth.test_support
from farnsworth.models import ChallengeBinaryNode

class TestChallengeBinaryNode:
    def setup(self):
        farnsworth.test_support.truncate_tables()

    def test_root_association(self):
        root_cbn = ChallengeBinaryNode.create(name = "root", cs_id = "foo")
        cbn1 = ChallengeBinaryNode.create(name = "test1", cs_id = "foo", root = root_cbn)
        cbn2 = ChallengeBinaryNode.create(name = "test2", cs_id = "foo", root = root_cbn)

        assert_equals(cbn1.root, root_cbn)
        assert_equals(len(root_cbn.descendants), 2)
        assert_in(cbn1, root_cbn.descendants)
        assert_in(cbn2, root_cbn.descendants)

    def test_parent_association(self):
        parent_cbn = ChallengeBinaryNode.create(name = "parent", cs_id = "foo")
        cbn1 = ChallengeBinaryNode.create(name = "test1", cs_id = "foo", parent = parent_cbn)
        cbn2 = ChallengeBinaryNode.create(name = "test2", cs_id = "foo", parent = parent_cbn)

        assert_equals(cbn1.parent, parent_cbn)
        assert_equals(len(parent_cbn.children), 2)
        assert_in(cbn1, parent_cbn.children)
        assert_in(cbn2, parent_cbn.children)
