#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os
import time

from nose.tools import *
from peewee import IntegrityError

from . import setup_each, teardown_each
from farnsworth.models import (ChallengeBinaryNode, ChallengeSet,
                               Round, Team, PatchType)
import farnsworth.models    # to avoid collisions between Test and nosetests

NOW = datetime.now()
BLOB = "blob data"
BLOB2 = "blob data2"
BLOB3 = "blob data3"
BLOB4 = "blob data4"
BLOB5 = "blob data5"


class TestChallengeBinaryNode:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_cs_name_and_sha256_uniqueness(self):
        cs1 = ChallengeSet.create(name="foo")
        cs2 = ChallengeSet.create(name="bar")
        # first binary is ok
        ChallengeBinaryNode.create(name="test1", cs=cs1, blob=BLOB)
        # same binary with different name is ok
        ChallengeBinaryNode.create(name="test2", cs=cs1, blob=BLOB)
        # same binary with different cs is ok
        ChallengeBinaryNode.create(name="test1", cs=cs2, blob=BLOB)
        # same cs and name but different binary is ok
        ChallengeBinaryNode.create(name="test1", cs=cs2, blob=BLOB2)
        # same cs, name and binary raises error
        assert_raises(IntegrityError, ChallengeBinaryNode.create, name="test1", cs=cs1, blob=BLOB)

    def test_root_association(self):
        cs = ChallengeSet.create(name="foo")
        root_cbn = ChallengeBinaryNode.create(name="root", cs=cs, blob=BLOB3)
        cbn1 = ChallengeBinaryNode.create(name="test1", cs=cs, root=root_cbn, blob=BLOB4)
        cbn2 = ChallengeBinaryNode.create(name="test2", cs=cs, root=root_cbn, blob=BLOB5)

        assert_equals(cbn1.root, root_cbn)
        assert_equals(len(root_cbn.descendants), 2)
        assert_in(cbn1, root_cbn.descendants)
        assert_in(cbn2, root_cbn.descendants)

    def test_binary_is_created_and_deleted_properly(self):
        cs = ChallengeSet.create(name=str(time.time()))
        cbn = ChallengeBinaryNode.create(name="mybin-%s" % cs.name, cs=cs, blob=BLOB)
        binpath = cbn._path

        assert_false(os.path.isfile(binpath))
        cbn.path

        assert_true(os.path.isfile(binpath))
        assert_equals(open(cbn.path, 'rb').read(), BLOB)
        cbn = None
        # FIXME
        # assert_false(os.path.isfile(binpath))

    def test_roots(self):
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="root1", cs=cs, blob=BLOB, sha256="sum1")
        cbn2 = ChallengeBinaryNode.create(name="root2", cs=cs, blob=BLOB, sha256="sum2")
        cbn3 = ChallengeBinaryNode.create(name="child", cs=cs, blob=BLOB, root=cbn1, sha256="sum3")

        assert_equals(len(ChallengeBinaryNode.roots()), 2)
        assert_in(cbn1, ChallengeBinaryNode.roots())
        assert_in(cbn2, ChallengeBinaryNode.roots())

    def test_all_descendants(self):
        cs = ChallengeSet.create(name="foo")
        cbn1 = ChallengeBinaryNode.create(name="root1", cs=cs, blob=BLOB, sha256="sum1")
        cbn2 = ChallengeBinaryNode.create(name="root2", cs=cs, blob=BLOB, sha256="sum2")
        cbn3 = ChallengeBinaryNode.create(name="child", cs=cs, blob=BLOB, root=cbn1, sha256="sum3")

        assert_equals(len(ChallengeBinaryNode.all_descendants()), 1)
        assert_in(cbn3, ChallengeBinaryNode.all_descendants())

    def test_submitted_and_unsubmitted_patches(self):
        r0 = Round.create(num=0)
        team = Team.create(name=Team.OUR_NAME)
        cs = ChallengeSet.create(name="foo")
        cs.rounds = [r0]
        cbn = ChallengeBinaryNode.create(name="cbn", cs=cs, blob="aaa1")
        patchtype1 = PatchType.create(name="PatchType1", functionality_risk=0, exploitability=0)
        patchtype2 = PatchType.create(name="PatchType2", functionality_risk=0, exploitability=0)

        patch1 = ChallengeBinaryNode.create(name="patch1", patch_type=patchtype1, cs=cs, root=cbn,
                                            blob="aaa2")
        patch2 = ChallengeBinaryNode.create(name="patch2", patch_type=patchtype2, cs=cs, root=cbn,
                                            blob="aaa3")

        assert_equals(len(cbn.unsubmitted_patches), 2)
        assert_in(patch1, cbn.unsubmitted_patches)
        assert_in(patch2, cbn.unsubmitted_patches)
        assert_equals(len(cbn.submitted_patches), 0)

        cs.submit(cbns=[patch1, patch2], round=r0)
        assert_equals(len(cbn.submitted_patches), 2)
        assert_equals(len(cbn.unsubmitted_patches), 0)
