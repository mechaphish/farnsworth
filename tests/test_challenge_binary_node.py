from nose.tools import *
import time
import os

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, ChallengeBinaryNode, ChallengeSet
import farnsworth.models # to avoid collisions between Test and nosetests

class TestChallengeBinaryNode:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_init(self):
        cs = ChallengeSet.find_or_create(name = 'foo')
        cbn1 = ChallengeBinaryNode.create(name = "test1", cs_id = "foo")
        cbn2 = ChallengeBinaryNode.create(name = "test1", cs = cs)
        assert_equals(cbn1.cs, cs)

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
        cbn = ChallengeBinaryNode.create(name = "mybin", cs_id = str(time.time()), blob="byte data")
        binpath = cbn._path
        assert_false(os.path.isfile(binpath))
        cbn.path
        assert_true(os.path.isfile(binpath))
        assert_equals(open(cbn.path, 'rb').read(), "byte data")
        cbn = None
        # FIXME
        # assert_false(os.path.isfile(binpath))

    def test_roots(self):
        cbn1 = ChallengeBinaryNode.create(name = "root1", cs_id = "foo", blob="data")
        cbn2 = ChallengeBinaryNode.create(name = "root2", cs_id = "foo", blob="data")
        cbn3 = ChallengeBinaryNode.create(name = "child", cs_id = "foo", blob="data", root = cbn1)

        assert_equals(len(ChallengeBinaryNode.roots()), 2)
        assert_in(cbn1, ChallengeBinaryNode.roots())
        assert_in(cbn2, ChallengeBinaryNode.roots())

    def test_all_descendants(self):
        cbn1 = ChallengeBinaryNode.create(name = "root1", cs_id = "foo", blob="data")
        cbn2 = ChallengeBinaryNode.create(name = "root2", cs_id = "foo", blob="data")
        cbn3 = ChallengeBinaryNode.create(name = "child", cs_id = "foo", blob="data", root = cbn1)

        assert_equals(len(ChallengeBinaryNode.all_descendants()), 1)
        assert_in(cbn3, ChallengeBinaryNode.all_descendants())

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

    def test_all_tests_for_this_cb(self):
        cbn = ChallengeBinaryNode.create(name = "cbn", cs_id = "foo", blob="data")
        patch1 = ChallengeBinaryNode.create(name = "patch1", cs_id = "foo", blob="data", root = cbn)
        job = AFLJob.create(cbn=cbn)
        test1 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="test1")
        test2 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="test2")

        assert_equals(len(patch1.tests), 0)
        assert_equals(len(patch1.all_tests_for_this_cb), 2)

    def test_found_crash_for_cb(self):
        cbn1 = ChallengeBinaryNode.create(name = "cbn1", cs_id = "foo", blob="data")
        cbn2 = ChallengeBinaryNode.create(name = "cbn2", cs_id = "foo", blob="data")

        job = AFLJob.create(cbn=cbn1)

        crash = farnsworth.models.Crash.create(cbn=cbn1, job=job, blob="crash")

        assert_true(cbn1.found_crash)
        assert_false(cbn2.found_crash)
