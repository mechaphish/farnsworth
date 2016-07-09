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
                                   ValidPoll, CbPollPerformance, PatchScore,
                                   RawRoundPoll, RawRoundTraffic,
                                   FunctionIdentity, TracerCache,
                                   ChallengeBinaryNodeFielding,
                                   ExploitFielding, IDSRuleFielding)
    models = [Round, Bitmap, ChallengeBinaryNode, ChallengeSet, Crash,
              Evaluation, Exploit, Feedback, FuzzerStat, IDSRule, Job, Pcap,
              Score, Team, Test, TesterResult, ValidPoll, CbPollPerformance,
              PatchScore, RawRoundPoll, RawRoundTraffic, FunctionIdentity,
              TracerCache, ChallengeBinaryNodeFielding, ExploitFielding,
              IDSRuleFielding]
    through_models = [ChallengeSet.rounds,
                      Feedback.round,
                      ChallengeBinaryNodeFielding.cbn,
                      ChallengeBinaryNodeFielding.team,
                      ChallengeBinaryNodeFielding.submission_round,
                      ChallengeBinaryNodeFielding.available_round,
                      ChallengeBinaryNodeFielding.fielded_round,
                      IDSRuleFielding.ids_rule,
                      IDSRuleFielding.team,
                      IDSRuleFielding.submission_round,
                      IDSRuleFielding.available_round,
                      IDSRuleFielding.fielded_round,
                      ExploitFielding.exploit,
                      ExploitFielding.team,
                      ExploitFielding.submission_round]

    return models + [tm.get_through_model() for tm in through_models]


def create_tables():
    LOG.debug("Creating tables...")
    master_db.create_tables(tables(), safe=True)


def drop_tables():
    LOG.debug("Dropping tables...")
    master_db.drop_tables(tables(), safe=True, cascade=True)
