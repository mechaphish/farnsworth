#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, ChallengeBinaryNode, ChallengeSet
import farnsworth.models    # to avoid collisions between Test and nosetests


class TestTest:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_cbn_association(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, blob="blob data", sha256="sum")
        job = AFLJob.create(cbn=cbn)
        test1 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="testicolo sn")
        test2 = farnsworth.models.Test.create(cbn=cbn, job=job, blob="testicolo dx")
        assert_equals(len(cbn.tests), 2)
        assert_in(test1, cbn.tests)
        assert_in(test2, cbn.tests)

    def test_cqe_pov_xml(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, blob="blob data", sha256="sum")
        job = AFLJob.create(cbn=cbn)
        test = farnsworth.models.Test.create(cbn=cbn, job=job, blob="XXX")
        test_xml = '''<?xml version="1.0" standalone="no" ?>
                        <!DOCTYPE pov SYSTEM "/usr/share/cgc-docs/replay.dtd">
                     <pov><cbid>{cbid}</cbid><replay><write><data>{data}</data></write></replay></pov>'''
        assert_equals(test.to_cqe_pov_xml(), test_xml.format(cbid=test.cbn.id, data='XXX'))
