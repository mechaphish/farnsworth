#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime

from peewee import ForeignKeyField, DateTimeField, IntegerField, BooleanField, CharField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

"""Job models"""


def to_job_type(job):
    """
    Cast a generic job to its proper subclass.

    Note: This function *modifies* the input job, but it also returns the
    modified one for convience.
    """
    job_types = [# Worker jobs, directly on Kubernetes
                 AFLJob, CacheJob, ColorGuardJob, DrillerJob, FunctionIdentifierJob, IDSJob,
                 NetworkPollCreatorJob, PatcherexJob, PovFuzzer1Job, PovFuzzer2Job, RexJob,
                 WereRabbitJob,
                 # Tester jobs
                 TesterJob, CBRoundTesterJob, CBTesterJob, NetworkPollSanitizerJob, PollCreatorJob]

    for job_type in job_types:
        if job.worker == job_type.worker.default:
            job.__class__ = job_type
            return job

    # Worker jobs, directly on Kubernetes
    #if job.worker == 'afl':
    #    job.__class__ = AFLJob
    #elif job.worker == 'cache':
    #    job.__class__ = CacheJob
    #elif job.worker == 'cb_round_tester':
    #    job.__class__ = CBRoundTesterJob
    #elif job.worker == 'colorguard':
    #    job.__class__ = ColorGuardJob
    #elif job.worker == 'driller':
    #    job.__class__ = DrillerJob
    #elif job.worker == 'function_identifier':
    #    job.__class__ = FunctionIdentifierJob
    #elif job.worker == 'ids':
    #    job.__class__ = IDSJob
    #elif job.worker == 'network_poll_creator':
    #    job.__class__ = NetworkPollCreatorJob
    #elif job.worker == 'patcherex':
    #    job.__class__ = PatcherexJob
    #elif job.worker == 'povfuzzer1':
    #    job.__class__ = PovFuzzer1Job
    #elif job.worker == 'povfuzzer2':
    #    job.__class__ = PovFuzzer2Job
    #elif job.worker == 'rex':
    #    job.__class__ = RexJob
    #elif job.worker == 'were_rabbit':
    #    job.__class__ = WereRabbitJob

    ## Tester jobs
    #elif job.worker == 'tester':
    #    job.__class__ = TesterJob
    #elif job.worker == 'cb_tester':
    #    job.__class__ = CBTesterJob
    #elif job.worker == 'network_poll_sanitizer':
    #    job.__class__ = NetworkPollSanitizerJob
    #elif job.worker == 'poll_creator':
    #    job.__class__ = PollCreatorJob
    return job


class Job(BaseModel):
    """Base Job model."""
    cbn = ForeignKeyField(ChallengeBinaryNode, null=True, related_name='jobs')
    completed_at = DateTimeField(null=True)
    limit_cpu = IntegerField(null=True, default=2)
    limit_memory = IntegerField(null=True, default=4096)    # MiB
    limit_time = IntegerField(null=True)                    # Seconds
    payload = BinaryJSONField(null=True)
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

    @classmethod
    def get_or_create(cls, **kwargs):
        return super(Job, cls).get_or_create(worker=cls.worker.default, **kwargs)


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


class AFLJob(Job):
    """This represents a job for AFL. It requires no extra input."""
    worker = CharField(default='afl')


class WereRabbitJob(Job):
    """This represents a job for AFL's Were Rabbit crash exploration mode."""
    worker = CharField(default='were_rabbit')


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
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_input_crash'):
            self._input_crash = None
        self._input_crash = self._input_crash or Crash.get(id=self.payload['crash_id'])
        # pylint: enable=attribute-defined-outside-init
        return self._input_crash


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


class PollCreatorJob(TesterJob):
    """
    This represents a job for Poller. Poller requires a testcase
    as an input. Here, we receive the testcase id as a string in the
    `payload` field.
    """
    worker = CharField(default='poll_creator')

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


class NetworkPollSanitizerJob(TesterJob):
    """
    This represents a job for NetworkPollSanitizer. NetworkPollSanitizer requires a
    untested network poll as an input. Here, we receive the raw_round_poll id as a string in the
    `payload` field.
    """
    worker = CharField(default='network_poll_sanitizer')

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


class CBTesterJob(Job):
    """
    This represents a job for cb_tester. cb_tester requires a cs, patch_type and a poll as an input.
    Here, we receive the poll id, cs id and patch_type as a strings in the `payload` field.
    """

    worker = CharField(default='cb_tester')

    @property
    def poll(self):
        """
        Get the poll that needs to be tested.
        :return: ValidPoll corresponding to this job.
        """
        from .valid_polls import ValidPoll
        if not hasattr(self, '_poll'):
            self._poll = None
        self._poll = self._poll or ValidPoll.get(id=self.payload['poll_id'])
        return self._poll

    @property
    def target_cs(self):
        """
        Get the target CS to which this tester job belongs to.
        :return: ChallengeSet object
        """
        from .challenge_set import ChallengeSet
        if not hasattr(self, '_target_cs'):
            self._target_cs = None
        self._target_cs = self._target_cs or ChallengeSet.get(id=self.payload['cs_id'])
        return self._target_cs

    @property
    def patch_type(self):
        """
        Get the patch type of the cb_tester job.
        :return: patch type as string.
        """
        if not hasattr(self, '_patch_type'):
            self._patch_type = None
        if 'patch_type' in self.payload:
            self._patch_type = self._patch_type or self.payload['patch_type']
        return self._patch_type


class CBRoundTesterJob(Job):
    """
    This represents a job for cb_round_tester. cb_round_tester a
    a round as an input. Here, we receive the round id as a strings in the
    `payload` field.

    This job indicates that testing need to be performed for all binaries
    against all network polls created from that round.
    """
    worker = CharField(default='cb_round_tester')

    @property
    def target_round(self):
        """
        Get the round for which testing needs to be done.
        :return: Target Round corresponding to this job.
        """
        from .round import Round
        if not hasattr(self, '_target_round'):
            self._target_round = None
        self._target_round = self._target_round or Round.get(id=self.payload['round_id'])
        return self._target_round


class NetworkPollCreatorJob(Job):
    """Create polls from captured network traffic."""
    worker = CharField(default='network_poll_creator')

    @property
    def target_round_traffic(self):
        """RawRoundTraffic that needs to be processed by this job."""
        # pylint:disable=attribute-defined-outside-init
        if not hasattr(self, '_target_round_traffic'):
            self._target_round_traffic = None
        from .raw_round_traffic import RawRoundTraffic
        self._target_round_traffic = self._target_round_traffic or RawRoundTraffic.find(self.payload['rrt_id'])
        # pylint: enable=attribute-defined-outside-init
        return self._target_round_traffic


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


class FunctionIdentifierJob(Job):
    """A FunctionIdentifierJob."""

    worker = CharField(default='function_identifier')


class CacheJob(Job):
    """A CacheJob."""

    worker = CharField(default='cache')
