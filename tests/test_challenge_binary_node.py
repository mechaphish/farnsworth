from nose.tools import *
import time
import os

from farnsworth.models import ChallengeBinaryNode

class TestChallengeBinaryNode:
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

    def test_binary_is_created_and_deleted_properly(self):
        cbn = ChallengeBinaryNode.create(name = "mybin", cs_id = int(time.time()), blob="byte data")
        binpath = cbn._path
        assert_false(os.path.isfile(binpath))
        cbn.path
        assert_true(os.path.isfile(binpath))
        assert_equals(open(cbn.path, 'rb').read(), "byte data")
        cbn = None
        assert_false(os.path.isfile(binpath))
