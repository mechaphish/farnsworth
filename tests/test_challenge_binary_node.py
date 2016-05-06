from nose.tools import *
import time
import os

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode

class TestChallengeBinaryNode:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

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

    def test_roots(self):
        cbn1 = ChallengeBinaryNode.create(name = "root1", cs_id = "foo", blob="data")
        cbn2 = ChallengeBinaryNode.create(name = "root2", cs_id = "foo", blob="data")
        cbn3 = ChallengeBinaryNode.create(name = "child", cs_id = "foo", blob="data", root = cbn1)

        assert_equals(len(ChallengeBinaryNode.roots()), 2)
        assert_in(cbn1, ChallengeBinaryNode.roots())
        assert_in(cbn2, ChallengeBinaryNode.roots())

    def test_unsubmitted_patches(self):
        cbn = ChallengeBinaryNode.create(name = "cbn", cs_id = "foo", blob="data")
        patch1 = ChallengeBinaryNode.create(name = "patch1", cs_id = "foo", blob="data", root = cbn)
        patch2 = ChallengeBinaryNode.create(name = "patch2", cs_id = "foo", blob="data", root = cbn)

        assert_equals(len(cbn.unsubmitted_patches), 2)
        assert_equals(patch1, cbn.unsubmitted_patches[0])
        assert_equals(patch2, cbn.unsubmitted_patches[1])

        patch1.submit()
        patch2.submit()
        assert_equals(len(cbn.unsubmitted_patches), 0)
