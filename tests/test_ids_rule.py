#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os
import time

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeSet, IDSRule


class TestIDSRule:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_submit(self):
        cs = ChallengeSet.create(name = "foo")
        ids = IDSRule.create(cs = cs, rules = "aaa")

        assert_is_none(ids.submitted_at)
        ids.submit()
        assert_is_instance(ids.submitted_at, datetime)
