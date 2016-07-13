#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import RexJob, ChallengeBinaryNode, RopCacheJob, RopCache, ChallengeBinaryNode, ChallengeSet


class TestRopCache:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_can_create(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="some_sha")
        job = RopCacheJob.get_or_create(cbn=cbn)
        rop_cache = RopCache.create(cbn=cbn, blob="asdf")
        assert_equals(str(rop_cache.blob), "asdf")
