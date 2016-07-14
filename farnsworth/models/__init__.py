#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import farnsworth.log


"""Farnsworth models"""

from .bitmap import Bitmap
from .cb_poll_performance import CBPollPerformance
from .challenge_binary_node_fielding import ChallengeBinaryNodeFielding
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_binary_node_fielding import ChallengeBinaryNodeFielding
from .challenge_set import ChallengeSet
from .crash import Crash
from .evaluation import Evaluation
from .exploit_fielding import ExploitFielding
from .exploit import Exploit
from .exploit_fielding import ExploitFielding
from .feedback import Feedback
from .function_identity import FunctionIdentity
from .fuzzer_stats import FuzzerStat
from .ids_rule_fielding import IDSRuleFielding
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
    PovFuzzer1Job,
    PovFuzzer2Job,
    RexJob,
    RopCacheJob,
    WereRabbitJob,

    # Tester jobs, inside VM inside Docker
    TesterJob,
    CBTesterJob,
    NetworkPollSanitizerJob,
    PollCreatorJob,
    PovTesterJob
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
from .tester_result import TesterResult
from .test import Test
from .tracer_cache import TracerCache
from .valid_polls import ValidPoll

LOG = farnsworth.log.LOG.getChild('models')
DeprecationWarning("Importing farnworth.models is deprecated. "
                   "Please import the models you need explicitly.")
