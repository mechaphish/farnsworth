#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import time
import os

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, ChallengeSet, IDSRule


class TestChallengeSet:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_unsubmitted_ids_rules(self):
        cs = ChallengeSet.create(name="foo")
        ids1 = IDSRule.create(cs=cs, rules="aaa")
        ids2 = IDSRule.create(cs=cs, rules="bbb", submitted_at=datetime.now())

        assert_equals(len(cs.unsubmitted_ids_rules), 1)
        assert_in(ids1, cs.unsubmitted_ids_rules)

    def test_cbns_by_patch_type(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs)
        cbn1 = ChallengeBinaryNode.create(name="foo1", cs=cs, patch_type="patch0")
        cbn2 = ChallengeBinaryNode.create(name="foo2", cs=cs, patch_type="patch0")
        cbn3 = ChallengeBinaryNode.create(name="foo3", cs=cs, patch_type="patch1")
        # FIXME: use assert_in
        assert_equals(['patch0', 'patch1'], sorted(cs.cbns_by_patch_type().keys()))
        assert_equals([cbn1, cbn2], cs.cbns_by_patch_type()['patch0'])
        assert_equals([cbn3], cs.cbns_by_patch_type()['patch1'])

    def test_cbns_unpatched(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs)
        cbn_extra = ChallengeBinaryNode.create(name="foo1", cs=cs, patch_type="patch0")
        cbn_extra_fixme_asap_please = ChallengeBinaryNode.create(name="foo1-team1", cs=cs)

        assert_equals(len(cs.cbns_unpatched), 1)
        assert_in(cbn, cs.cbns_unpatched)
        assert_not_in(cbn_extra, cs.cbns_unpatched)
        assert_not_in(cbn_extra_fixme_asap_please, cs.cbns_unpatched)
