#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Job models"""

import datetime

from peewee import *    # pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import JSONField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

def to_job_type(job):
    """
    Cast a generic job to its proper subclass.

    Note: This function *modifies* the input job, but it also returns the
    modified one for convience.
    """
    if job.worker == 'afl':
        job.__class__ = AFLJob
    elif job.worker == 'driller':
        job.__class__ = DrillerJob
    elif job.worker == 'rex':
        job.__class__ = RexJob
    elif job.worker == 'patcherex':
        job.__class__ = PatcherexJob
    elif job.worker == 'tester':
        job.__class__ = TesterJob
    return job


class Job(BaseModel):
    """Base Job model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', to_field='id',
                          related_name='jobs')
    completed_at = DateTimeField(null=True)
    limit_cpu = IntegerField(null=True)
    limit_memory = IntegerField(null=True)
    limit_time = IntegerField(null=True)
    payload = JSONField()
    priority = IntegerField()
    produced_output = BooleanField(null=True)
    started_at = DateTimeField(null=True)
    worker = CharField()

    class Meta:     # pylint:disable=no-init,missing-docstring,old-style-class
        def db_table_func(self):   # pylint:disable=no-self-argument,no-self-use
            return 'jobs'

    def started(self):
        """Mark job as started"""
        self.started_at = datetime.datetime.now()
        self.save()

    def is_started(self):
        """Check if job is started"""
        return self.started_at is not None

    def is_completed(self):
        """Check if job is completed"""
        return self.completed_at is not None

    def completed(self):
        """Mark job as completed"""
        self.completed_at = datetime.datetime.now()
        self.save()

    @classmethod
    def unstarted(cls):
        """Return all unstarted jobs"""
        return cls.select().where(cls.started_at.is_null(True) & (cls.worker == cls.worker.default))


class DrillerJob(Job):
    """
    This represents a job for driller. Driller requires a testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='driller')

    @property
    def input_test(self):
        """Return input test case"""
        from .test import Test
        if not hasattr(self, '_input_test'):
            self._input_test = None # pylint:disable=attribute-defined-outside-init
        self._input_test = self._input_test or Test.get(id=self.payload['test_id']) # pylint:disable=attribute-defined-outside-init
        return self._input_test

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'driller') &
                    (cls.payload['test_id'] == str(job.payload['test_id'])))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False


class AFLJob(Job):
    """This represents a job for AFL. It requires no extra input."""
    worker = CharField(default='afl')

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'afl') &
                    cls.completed_at.is_null(True))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False


class RexJob(Job):
    """
    This represents a job for rex. Rex requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='rex')

    @property
    def input_crash(self):
        """Return input crash"""
        from .crash import Crash
        if not hasattr(self, '_input_crash'):
            self._input_crash = None # pylint:disable=attribute-defined-outside-init
        self._input_crash = self._input_crash or Crash.get(id=self.payload['crash_id']) # pylint:disable=attribute-defined-outside-init
        return self._input_crash

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'rex') &
                    (cls.payload['crash_id'] == str(job.payload['crash_id'])))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False


class PatcherexJob(Job):
    """A PatcherexJob."""
    worker = CharField(default='patcherex')

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'patcherex'))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False


class TesterJob(Job):
    """
    This represents a job for Tester. Tester requires a testcase
    as an input. Here, we receive the testcase id as a string in the
    `payload` field.
    """

    worker = CharField(default='tester')

    @property
    def target_test(self):
        """
        Get the target test corresponding to this tester job
        :return: Test corresponding to this job.
        """
        from .test import Test
        if not hasattr(self, '_target_test'):
            self._target_test = None # pylint:disable=attribute-defined-outside-init
        self._target_test = self._target_test or Test.get(id=self.payload['test_id']) # pylint:disable=attribute-defined-outside-init
        return self._target_test

    def mark_job_not_started(self):
        """
        Mark this current job as not started.
        This is required in case, the job incurred an schrodinger failure.
        :return: None
        """
        self.started_at = DateTimeField(null=True)
        self.completed_at = DateTimeField(null=True)
        self.save()

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'tester') &
                    (cls.payload['test_id'] == str(job.payload['test_id'])))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False
