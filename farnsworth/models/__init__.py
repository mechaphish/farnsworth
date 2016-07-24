#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import farnsworth.log


"""Farnsworth models"""

from .bitmap import Bitmap
from .cb_poll_performance import CBPollPerformance
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set import ChallengeSet
from .challenge_set_fielding import ChallengeSetFielding
from .cs_submission_cable import CSSubmissionCable
from .crash import Crash
from .evaluation import Evaluation
from .exploit import Exploit
from .exploit_fielding import ExploitFielding
from .exploit_submission_cable import ExploitSubmissionCable
from .feedback import Feedback
from .function_identity import FunctionIdentity
from .fuzzer_stats import FuzzerStat
from .ids_rule import IDSRule
from .ids_rule_fielding import IDSRuleFielding
from .job import (
    to_job_type,
    Job,
    # Worker jobs, inside Docker
    AFLJob,
    CacheJob,
    CBRoundTesterJob,
    ColorGuardJob,
    DrillerJob,
    FunctionIdentifierJob,
    IDSJob,
    PatcherexJob,
    NetworkPollCreatorJob,
    PatchPerformanceJob,
    PovFuzzer1Job,
    PovFuzzer2Job,
    RexJob,
    RopCacheJob,
    BackdoorSubmitterJob,

    # Tester jobs, inside VM inside Docker
    TesterJob,
    CBTesterJob,
    NetworkPollSanitizerJob,
    PollCreatorJob,
    PovTesterJob,
    ShowmapSyncJob
)
from .patch_score import PatchScore
from .pcap import Pcap
from .pov_test_result import PovTestResult
from .raw_round_poll import RawRoundPoll
from .raw_round_traffic import RawRoundTraffic
from .rop_cache import RopCache
from .round import Round
from .score import Score
from .team import Team
from .test import Test
from .tester_result import TesterResult
from .tracer_cache import TracerCache
from .valid_polls import ValidPoll

LOG = farnsworth.log.LOG.getChild('models')
DeprecationWarning("Importing farnworth.models is deprecated. "
                   "Please import the models you need explicitly.")
