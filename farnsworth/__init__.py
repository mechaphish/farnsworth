#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Farnsworth database setup."""

from __future__ import absolute_import, unicode_literals

from .config import master_db
from .log import LOG


def tables():
    from farnsworth.models import (Bitmap,
                                   CBPollPerformance,
                                   CSSubmissionCable,
                                   ChallengeBinaryNode,
                                   ChallengeSet,
                                   ChallengeSetFielding,
                                   Crash,
                                   Evaluation,
                                   Exploit,
                                   ExploitFielding,
                                   ExploitSubmissionCable,
                                   Feedback,
                                   FunctionIdentity,
                                   FuzzerStat,
                                   IDSRule,
                                   IDSRuleFielding,
                                   Job,
                                   PatchScore,
                                   PatchType,
                                   Pcap,
                                   PollFeedback,
                                   PovTestResult,
                                   RawRoundPoll,
                                   RawRoundTraffic,
                                   RopCache,
                                   Round,
                                   Score,
                                   Team,
                                   Test,
                                   TesterResult,
                                   TracerCache,
                                   ValidPoll)
    models = [Bitmap,
              CBPollPerformance,
              ChallengeBinaryNode,
              ChallengeSet,
              ChallengeSetFielding,
              CSSubmissionCable,
              Crash,
              Evaluation,
              Exploit,
              ExploitFielding,
              ExploitSubmissionCable,
              Feedback,
              FunctionIdentity,
              FuzzerStat,
              IDSRule,
              IDSRuleFielding,
              Job,
              PatchScore,
              PatchType,
              Pcap,
              PovTestResult,
              PollFeedback,
              RawRoundPoll,
              RawRoundTraffic,
              RopCache,
              Round,
              Score,
              Team,
              Test,
              TesterResult,
              TracerCache,
              ValidPoll]
    through_models = [ChallengeSet.rounds,
                      ChallengeSetFielding.cbns,
                      CSSubmissionCable.cbns]
    return models + [tm.get_through_model() for tm in through_models]

def create_tables():
    LOG.debug("Creating tables...")
    master_db.create_tables(tables(), safe=True)

    from farnsworth.models import (ChallengeBinaryNode,
                                   ChallengeSetFielding,
                                   Crash,
                                   ExploitSubmissionCable,
                                   IDSRule,
                                   IDSRuleFielding,
                                   Test)
    master_db.create_index(ChallengeBinaryNode, ['cs', 'name', 'sha256'], unique=True)
    master_db.create_index(ChallengeSetFielding, ['cs', 'team', 'submission_round'], unique=True)
    master_db.create_index(ChallengeSetFielding, ['cs', 'team', 'available_round'], unique=True)
    master_db.create_index(Crash, ['cs', 'sha256'], unique=True)
    master_db.create_index(Test, ['cs', 'sha256'], unique=True)
    master_db.create_index(ChallengeSetFielding, ['sha256'])
    master_db.create_index(ChallengeBinaryNode, ['sha256'])
    master_db.create_index(Crash, ['sha256'])
    master_db.create_index(IDSRule, ['sha256'])
    master_db.create_index(IDSRuleFielding, ['sha256'])
    master_db.create_index(Test, ['sha256'])
    master_db.create_index(ExploitSubmissionCable, ['cs', 'team'], unique=True)

    LOG.debug("Creating patch types...")
    from farnsworth.models import PatcherexJob, PatchType
    for name, (func_risk, exploitability) in PatcherexJob.PATCH_TYPES.items():
        PatchType.create(name=name, functionality_risk=func_risk, exploitability=exploitability)

def drop_tables():
    LOG.debug("Dropping tables...")
    master_db.drop_tables(tables(), safe=True, cascade=True)
