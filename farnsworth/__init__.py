#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from .config import master_db
from .log import LOG

"""Farnsworth database setup."""


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
                                   Test)
    master_db.create_index(ChallengeBinaryNode, ['cs', 'name', 'sha256'], unique=True)
    master_db.create_index(ChallengeSetFielding, ['cs', 'team', 'submission_round'], unique=True)
    master_db.create_index(ChallengeSetFielding, ['cs', 'team', 'available_round'], unique=True)
    master_db.create_index(ChallengeSetFielding, ['cs', 'team', 'fielded_round'], unique=True)
    master_db.create_index(Crash, ['cs', 'sha256'], unique=True)
    master_db.create_index(Test, ['cs', 'sha256'], unique=True)

def drop_tables():
    LOG.debug("Dropping tables...")
    master_db.drop_tables(tables(), safe=True, cascade=True)
