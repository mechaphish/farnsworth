#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from .config import master_db
from .log import LOG

from farnsworth.models import (Round, Bitmap, ChallengeBinaryNode,
                               ChallengeSet, Crash, Evaluation, Exploit,
                               Feedback, FuzzerStat, IDSRule, Job, Pcap,
                               Score, Team, Test, TesterResult,
                               ValidPoll, CbPollPerformance, PatchScore,
                               RawRoundPoll, RawRoundTraffic,
                               FunctionIdentity, TracerCache,
                               ChallengeBinaryNodeFielding,
                               ExploitFielding, IDSRuleFielding)
"""Farnsworth database setup."""


def tables():
    models = [Round, Bitmap, ChallengeBinaryNode, ChallengeSet, Crash,
              Evaluation, Exploit, Feedback, FuzzerStat, IDSRule, Job, Pcap,
              Score, Team, Test, TesterResult, ValidPoll, CbPollPerformance,
              PatchScore, RawRoundPoll, RawRoundTraffic, FunctionIdentity,
              TracerCache, ChallengeBinaryNodeFielding, ExploitFielding,
              IDSRuleFielding]
    through_models = [ChallengeSet.rounds,
                      ChallengeBinaryNodeFielding.team,
                      IDSRuleFielding.team,
                      ExploitFielding.team]
    return models + [tm.get_through_model() for tm in through_models]

def create_tables():
    LOG.debug("Creating tables...")
    master_db.create_tables(tables(), safe=True)
    master_db.create_index(ChallengeBinaryNode, ['sha256'], unique=True)

def drop_tables():
    LOG.debug("Dropping tables...")
    master_db.drop_tables(tables(), safe=True, cascade=True)
