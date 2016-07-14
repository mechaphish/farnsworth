#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from .config import master_db
from .log import LOG

"""Farnsworth database setup."""


def tables():
    from farnsworth.models import (Round, Bitmap, ChallengeBinaryNode,
                                   ChallengeSet, Crash, Evaluation, Exploit,
                                   Feedback, FuzzerStat, IDSRule, Job, Pcap,
                                   Score, Team, Test, TesterResult,
                                   ValidPoll, CBPollPerformance, PatchScore,
                                   RawRoundPoll, RawRoundTraffic,
                                   FunctionIdentity, TracerCache,
                                   ChallengeBinaryNodeFielding,
                                   ExploitFielding, IDSRuleFielding, PovTestResult)
    models = [Round, Bitmap, ChallengeBinaryNode, ChallengeSet, Crash,
              Evaluation, Exploit, Feedback, FuzzerStat, IDSRule, Job, Pcap,
              Score, Team, Test, TesterResult, ValidPoll, CBPollPerformance,
              PatchScore, RawRoundPoll, RawRoundTraffic, FunctionIdentity,
              TracerCache, ChallengeBinaryNodeFielding, ExploitFielding,
              IDSRuleFielding, PovTestResult]
    through_models = [ChallengeSet.rounds]
    return models + [tm.get_through_model() for tm in through_models]

def create_tables():
    LOG.debug("Creating tables...")
    master_db.create_tables(tables(), safe=True)

    from farnsworth.models import ChallengeBinaryNode
    master_db.create_index(ChallengeBinaryNode, ['sha256'], unique=True)

def drop_tables():
    LOG.debug("Dropping tables...")
    master_db.drop_tables(tables(), safe=True, cascade=True)
