#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime

from peewee import ForeignKeyField, DateTimeField, IntegerField, BooleanField, CharField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .challenge_set import ChallengeSet
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set_fielding import ChallengeSetFielding
from .ids_rule_fielding import IDSRuleFielding

"""Job models"""


def to_job_type(job):
    """
    Cast a generic job to its proper subclass.

    Note: This function *modifies* the input job, but it also returns the
    modified one for convience.
    """
    job_types = [# Worker jobs, directly on Kubernetes
                 AFLJob, BackdoorSubmitterJob, CacheJob, CBRoundTesterJob, ColorGuardJob,
                 DrillerJob, FunctionIdentifierJob, IDSJob, NetworkPollCreatorJob,
                 PatchPerformanceJob, PatcherexJob, PovFuzzer1Job, PovFuzzer2Job, RexJob,
                 RopCacheJob,
                 # Tester jobs
                 TesterJob, CBTesterJob, NetworkPollSanitizerJob, PollCreatorJob,
                 PovTesterJob, ShowmapSyncJob]

    for job_type in job_types:
        if job.worker == job_type.worker.default:
            job.__class__ = job_type
            return job

    raise TypeError("Invalid Job object passed")


class Job(BaseModel):
    """Base Job model."""
    cs = ForeignKeyField(ChallengeSet, null=True, related_name='jobs')
    cbn = ForeignKeyField(ChallengeBinaryNode, null=True, related_name='jobs')
    completed_at = DateTimeField(null=True)
    request_cpu = IntegerField(null=True, default=1)
    request_memory = IntegerField(null=True, default=2048)  # MiB
    limit_cpu = IntegerField(null=True, default=2)
    limit_memory = IntegerField(null=True, default=4096)    # MiB
    limit_time = IntegerField(null=True)                    # Seconds
    payload = BinaryJSONField(null=True)
    priority = IntegerField(null=False, default=0)
    produced_output = BooleanField(null=True)
    started_at = DateTimeField(null=True)
    worker = CharField()
    kvm_access = False
    data_access = False
    restart = True

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
    restart = False

    @property
    def input_test(self):
        """Return input test case"""
        from .test import Test
        # pylint:disable=attribute-defined-outside-init
        if not hasattr(self, '_input_test'):
            self._input_test = None

        if self._input_test is None:
            self._input_test = Test.get(id=self.payload['test_id'])

        return self._input_test


class ColorGuardJob(Job):
    """
    This represents a job for ColorGuard. It requires a testcase
    as an input.
    """

    worker = CharField(default='colorguard')
    restart = False

    @property
    def input_test(self):
        """Return input test case"""
        from .test import Test
        # pylint:disable=attribute-defined-outside-init
        if not hasattr(self, '_input_test'):
            self._input_test = None

        if self._input_test is None:
            self._input_test = Test.get(id=self.payload['test_id'])

        return self._input_test


class AFLJob(Job):
    """This represents a job for AFL. It requires no extra input."""
    worker = CharField(default='afl')

    @property
    def challenge_set(self):
        """Return challenge set to fuzz"""
        # pylint:disable=attribute-defined-outside-init
        if not hasattr(self, '_challenge_set'):
            self._challenge_set = None

        if self._challenge_set is None:
            self._challenge_set = ChallengeSet.get(id=self.payload['cs_id'])

        return self._challenge_set

class RexJob(Job):
    """
    This represents a job for rex. Rex requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """
    worker = CharField(default='rex')
    restart = False

    @property
    def input_crash(self):
        """Return input crash"""
        from .crash import Crash
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_input_crash'):
            self._input_crash = None

        if self._input_crash is None:
            self._input_crash = Crash.get(id=self.payload['crash_id'])

        return self._input_crash


class PovFuzzer1Job(RexJob):
    """
    This represents a job for rex. PovFuzzer1 requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='povfuzzer1')
    kvm_access = True
    data_access = True
    restart = False


class PovFuzzer2Job(RexJob):
    """
    This represents a job for rex. PovFuzzer2 requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='povfuzzer2')
    kvm_access = True
    data_access = True
    restart = False


class PatcherexJob(Job):
    """A PatcherexJob."""

    # the risks and exploitability associated with every patch type
    PATCH_TYPES = {
        "voidpartialbitflip": (0.1, 0.9),
        "medium_detour": (0.3, 0.5),
        "medium_reassembler": (0.2, 0.5),
        "medium_detour_fidget": (0.25, 0.5),
        "medium_reassembler_fidget": (0.23, 0.5),
        "light_detour": (0.23, 0.8),
        "light_reassembler": (0.22, 0.8),
        "optimized": (0.22, 0.8)
    }

    worker = CharField(default='patcherex')


class TesterJob(Job):
    """
    This represents a job for Tester. Tester requires a testcase
    as an input. Here, we receive the testcase id as a string in the
    `payload` field.
    """

    worker = CharField(default='tester')
    kvm_access = True
    data_access = True

    def mark_test_not_completed(self):
        """
        Mark the provided job as not completed, that is as Failed.

        :return: True if successful else False
        """
        if self.is_started():
            self.started_at = None
            self.completed_at = None
            self.save()
            return True
        return False

    @classmethod
    def unstarted(cls, cs):
        """Return all unstarted jobs for the provided ChallengeSet
        :param cs: ChallengeSet for which Jobs need to be fetched.
        :return List of job objects which are not started
        """
        return cls.select().where(cls.started_at.is_null(True)
                                  & (cls.worker == cls.worker.default)
                                  & (cls.cs == cs))


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
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_test'):
            self._target_test = None

        if self._target_test is None:
            self._target_test = Test.get(id=self.payload['test_id'])

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
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_round_poll'):
            self._round_poll = None

        if self._round_poll is None:
            self._round_poll = RawRoundPoll.get(id=self.payload['rrp_id'])

        return self._round_poll


class CBTesterJob(TesterJob):
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
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_poll'):
            self._poll = None

        if self._poll is None:
            self._poll = ValidPoll.get(id=self.payload['poll_id'])

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
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_patch_type'):
            self._patch_type = None

        if 'patch_type' in self.payload and self._patch_type is None:
            self._patch_type = self.payload['patch_type']

        return self._patch_type


class PatchPerformanceJob(Job):
    """
        This represents a Job for aggregating all performance
        measurements for all patched binaries for a specific round.
    """
    worker = CharField(default='patch_performance')

    @property
    def target_round(self):
        """
        Get the round number for until which performance need to be computed..
        :return: Round for which patch performance need to be computed.
        """
        from .round import Round
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_round'):
            self._target_round = None

        if self._target_round is None:
            self._target_round = Round.get(id=self.payload['round_id'])

        return self._target_round


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
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_round'):
            self._target_round = None

        if self._target_round is None:
            self._target_round = Round.get(id=self.payload['round_id'])

        return self._target_round


class NetworkPollCreatorJob(Job):
    """Create polls from captured network traffic."""
    worker = CharField(default='network_poll_creator')

    @property
    def target_round_traffic(self):
        """RawRoundTraffic that needs to be processed by this job."""
        from .raw_round_traffic import RawRoundTraffic
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_round_traffic'):
            self._target_round_traffic = None

        if self._target_round_traffic is None:
            self._target_round_traffic = RawRoundTraffic.find(self.payload['rrt_id'])

        return self._target_round_traffic


class PovTesterJob(TesterJob):
    """
    This represents a job for PovTester. PovTester requires a
    Exploit ID, CS Fielding ID, IDS Fielding ID as an input.
    """
    worker = CharField(default='pov_tester')

    @property
    def target_exploit(self):
        """
        Get the Exploit that needs to be tested.
        :return: Exploit corresponding to this job.
        """
        from .exploit import Exploit
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_exploit'):
            self._target_exploit = None

        if self._target_exploit is None:
            self._target_exploit = Exploit.get(id=self.payload['exploit_id'])

        return self._target_exploit

    @property
    def target_cs_fielding(self):
        """
        Get the CS Fielding associated with this Job.
        :return: CS Fielding object.
        """
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_cs_fielding'):
            self._target_cs_fielding = None

        if self._target_cs_fielding is None:
            self._target_cs_fielding = ChallengeSetFielding.get(ChallengeSetFielding.sha256 == self.payload['cs_fld_hash'])

        return self._target_cs_fielding

    @property
    def target_ids_fielding(self):
        """
        Get the IDS Fielding associated with this Job.
        :return: IDS Fielding object.
        """
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_target_ids_fielding'):
            self._target_ids_fielding = None

        if 'ids_fld_hash' in self.payload and self._target_ids_fielding is None:
            self._target_ids_fielding = IDSRuleFielding.get(IDSRuleFielding.sha256 == self.payload['ids_fld_hash'])

        return self._target_ids_fielding


class IDSJob(Job):
    """A IDSJob."""
    worker = CharField(default='ids')

    @property
    def cs(self):
        """Return input ChallengeSet"""
        from .challenge_set import ChallengeSet
        # pylint:disable=attribute-defined-outside-init
        if not hasattr(self, '_cs'):
            self._cs = None

        if self._cs is None:
            self._cs = ChallengeSet.find(self.payload.get('cs_id'))

        return self._cs


class FunctionIdentifierJob(Job):
    """A FunctionIdentifierJob."""

    worker = CharField(default='function_identifier')
    restart = False


class CacheJob(Job):
    """A CacheJob."""

    worker = CharField(default='cache')
    restart = False

    @property
    def atoi_flag(self):
        """Return whether or not to run with symbols"""
        if not hasattr(self, '_atoi_flag'):
            self._atoi_flag = None

        if self._atoi_flag is None:
            self._atoi_flag = self.payload['with_atoi']

        return self._atoi_flag


class RopCacheJob(Job):
    """A RopCacheJob."""

    worker = CharField(default='rop_cache')
    restart = False


class ShowmapSyncJob(Job):
    """A ShowMapSync."""

    worker = CharField(default='showmap_sync')
    restart = False

    @property
    def input_round(self):
        """Return input crash"""
        from .round import Round
        # pylint: disable=attribute-defined-outside-init
        if not hasattr(self, '_input_round'):
            self._input_round = None

        if self._input_round is None:
            self._input_round = Round.get(id=self.payload['round_id'])

        return self._input_round


class BackdoorSubmitterJob(Job):
    """A BackdoorSubmitterJob."""

    worker = CharField(default='backdoor_submitter')
    restart = False
