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
        rop_cache = RopCache.create(cs=cs, blob="asdf")
        assert_equals(str(rop_cache.blob), "asdf")
