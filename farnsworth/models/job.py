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
    elif job.worker == 'ids':
        job.__class__ = IDSJob
    elif job.worker == 'were_rabbit':
        job.__class__ = WereRabbitJob
    elif job.worker == 'colorguard':
        job.__class__ = ColorGuardJob
    elif job.worker == 'povfuzzer1':
        job.__class__ = PovFuzzer1Job
    elif job.worker == 'povfuzzer2':
        job.__class__ = PovFuzzer2Job
    elif job.worker == 'network_poll':
        job.__class__ = NetworkPollJob
    elif job.worker == 'pollsanitizer':
        job.__class__ = PollSanitizerJob

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
    priority = IntegerField(null=False, default=0)
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

    def try_start(self):
        """
        Mark the provide job as started, only if it not started before.
        :return: True if successful else false
        """

        if not self.is_started():
            self.started()
            return True
        return False

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


class ColorGuardJob(Job):
    """
    This represents a job for ColorGuard. It requires a testcase
    as an input.
    """

    worker = CharField(default='colorguard')

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
                    (cls.worker == 'colorguard') &
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


class WereRabbitJob(Job):
    """This represents a job for AFL's Were Rabbit crash exploration mode."""
    worker = CharField(default='were_rabbit')

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'were_rabbit') &
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
                    (cls.worker == cls.worker.default) &
                    (cls.payload['crash_id'] == str(job.payload['crash_id'])))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False

class PovFuzzer1Job(RexJob):
    """
    This represents a job for rex. PovFuzzer1 requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='povfuzzer1')

class PovFuzzer2Job(RexJob):
    """
    This represents a job for rex. PovFuzzer2 requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='povfuzzer2')

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

    def mark_testjob_not_completed(self):
        """
        Mark the provided job as not completed.
        i.e Failed
        :return: True if successful else false
        """
        if self.is_started():
            self.started_at = DateTimeField(null=True)
            self.completed_at = DateTimeField(null=True)
            self.save()
            return True
        return False

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


class PollerJob(Job):
    """
    This represents a job for Poller. Poller requires a testcase
    as an input. Here, we receive the testcase id as a string in the
    `payload` field.
    """
    worker = CharField(default='poller')

    @property
    def target_test(self):
        """
        Get the target test corresponding to this Poller job
        :return: Test corresponding to this job.
        """
        from .test import Test
        if not hasattr(self, '_target_test'):
            self._target_test = None
        self._target_test = self._target_test or Test.get(id=self.payload['test_id'])
        return self._target_test

    @classmethod
    def queued(cls, job):
        try:
            cls.get((cls.worker == 'poller') &
                    (cls.payload['test_id'] == str(job.payload['test_id'])))
            return True
        except cls.DoesNotExist:
            return False


class PollSanitizerJob(Job):
    """
    This represents a job for NetworkPollSanitizer. NetworkPollSanitizer requires a
    untested network poll as an input. Here, we receive the raw_round_poll id as a string in the
    `payload` field.
    """
    worker_name = 'pollsanitizer'
    worker = CharField(default=worker_name)

    @property
    def raw_poll(self):
        """
        Get the raw round poll that needs to be tested.
        :return: RawRoundPoll corresponding to this job.
        """
        from .raw_round_poll import RawRoundPoll
        if not hasattr(self, '_round_poll'):
            self._round_poll = None
        self._round_poll = self._round_poll or RawRoundPoll.get(id=self.payload['rrp_id'])
        return self._round_poll

    @classmethod
    def queued(cls, job):
        try:
            cls.get((cls.worker == PollSanitizerJob.worker_name) &
                    (cls.payload['rrp_id'] == str(job.payload['rrp_id'])))
            return True
        except cls.DoesNotExist:
            return False


class NetworkPollJob(Job):
    """ A Job to create polls from captured network traffic.
    """
    worker = CharField(default='network_poll')

    @property
    def target_round_traffic(self):
        """Return RawRoundTraffic to be processed by this job"""
        if not hasattr(self, '_target_round_traffic'):
            self._target_round_traffic = None # pylint:disable=attribute-defined-outside-init
        # pylint:disable=attribute-defined-outside-init
        from .raw_round_traffic import RawRoundTraffic
        self._target_round_traffic = self._target_round_traffic or RawRoundTraffic.find(self.payload['rrt_id'])
        return self._target_round_traffic

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.worker == cls.worker.default) &
                    (cls.payload['rrt_id'] == str(job.payload['rrt_id'])))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False


class IDSJob(Job):
    """A IDSJob."""
    worker = CharField(default='ids')

    @property
    def cs(self):
        """Return input ChallengeSet"""
        from .challenge_set import ChallengeSet
        if not hasattr(self, '_cs'):
            self._cs = None # pylint:disable=attribute-defined-outside-init
        self._cs = self._cs or ChallengeSet.find(self.payload.get('cs_id')) # pylint:disable=attribute-defined-outside-init
        return self._cs

    @classmethod
    def queued(cls, job):
        """Return true if job is already queued"""
        try:
            cls.get((cls.worker == 'ids') &
                    (cls.payload['cs_id'] == str(job.payload['cs_id'])))
            return True
        except cls.DoesNotExist: # pylint:disable=no-member
            return False
