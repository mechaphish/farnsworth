#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, RexJob, ChallengeBinaryNode

class TestAFLJob:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()
