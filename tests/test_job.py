#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime

from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import ChallengeBinaryNode, ChallengeSet
from farnsworth.models.job import *


class TestJob:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()

    def test_to_job_type(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum")
        afl_job = AFLJob.create(cbn=cbn)
        driller_job = DrillerJob.create(cbn=cbn)
        patcherex_job = PatcherexJob.create(cbn=cbn)
        rex_job = RexJob.create(cbn=cbn)
        tester_job = TesterJob.create(cbn=cbn)

        jobs = Job.select().order_by(Job.id.asc())
        job_types = [AFLJob, DrillerJob, PatcherexJob, RexJob, TesterJob]
        for i in range(len(job_types)):
            job_type = to_job_type(jobs[i]).__class__
            assert_in(job_type, job_types)
            job_types.remove(job_type)


    def test_added_completed(self):
        class GenericJob(Job):
            worker = CharField(default='generic_job')

        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum")
        job = GenericJob(cbn=cbn)
        assert_raises(GenericJob.DoesNotExist, GenericJob.get, GenericJob.cbn == cbn)

        useless_job = RexJob(cbn=cbn)
        assert_raises(GenericJob.DoesNotExist, GenericJob.get, GenericJob.cbn == cbn)

        job.save()
        job = GenericJob.get(GenericJob.cbn == cbn)

        job.completed_at = datetime.datetime.now()
        job.save()
        assert_raises(GenericJob.DoesNotExist, GenericJob.get,
                      GenericJob.cbn == cbn,
                      GenericJob.completed_at == None)

    def test_get_or_create(self):
        cs = ChallengeSet.create(name="foo")
        cbn = ChallengeBinaryNode.create(name="foo", cs=cs, sha256="sum")
        job1, job1_created = RexJob.get_or_create(cbn=cbn, payload={'something': 'xxx'})
        job2, job2_created = AFLJob.get_or_create(cbn=cbn, payload={'something': 'xxx'})

        assert_not_equal(job1.id, job2.id)
        assert_true(job1_created)
        assert_true(job2_created)

        job2.delete_instance(recursive=True)
        job1.delete_instance(recursive=True)
        cbn.delete_instance(recursive=True)
        cs.delete_instance(recursive=True)
        Job._meta.database.commit()
