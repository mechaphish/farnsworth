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
                                   FunctionIdentity, TracerCache)
    return [Round, Bitmap, ChallengeBinaryNode, ChallengeSet, Crash, Evaluation,
            Exploit, Feedback, FuzzerStat, IDSRule, Job, Pcap, Score, Team,
            Test, TesterResult, ValidPoll, CbPollPerformance, PatchScore,
            RawRoundPoll, RawRoundTraffic, FunctionIdentity, TracerCache]


def create_tables():
    LOG.debug("Creating tables...")
    master_db.create_tables(tables(), safe=True)


def drop_tables():
    LOG.debug("Dropping tables...")
    master_db.drop_tables(tables(), safe=True, cascade=True)
