#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import IntegerField, TextField, ForeignKeyField

from .base import BaseModel
from .exploit import Exploit
from .challenge_set_fielding import ChallengeSetFielding
from .ids_rule_fielding import IDSRuleFielding

"""PovTestResult model"""


class PovTestResult(BaseModel):
    """
    Result of a Pov Tested against a team with an ids_rules.
    """
    exploit = ForeignKeyField(Exploit, related_name='pov_test_results')
    cs_fielding = ForeignKeyField(ChallengeSetFielding, related_name='cs_fielding')
    ids_fielding = ForeignKeyField(IDSRuleFielding, related_name='ids_fielding', null=True)
    # Number of times Pov Succeeded out of 10 throws.
    num_success = IntegerField(default=0)
    # Feedback from Pov Testing, this could be used by Pov Fuzzer.
    test_feedback = TextField(null=True)

    @classmethod
    def best(cls, cs_fielding, ids_fielding):
        """Get best PoV test results for the provided cs fielding and ids fielding.

        :param cs_fielding: CS fielding for which PoVTestResult need to be fetched.
        :param ids_fielding: IDS fielding for which PoVTestResult need to be fetched.
        :return: List containing best PoV test result.
        """
        query = cls.select(cls).join(ChallengeSetFielding)
        predicate = ChallengeSetFielding.sha256 == cs_fielding.sha256

        if ids_fielding is None:
            predicate &= cls.ids_fielding.is_null(True)
        else:
            predicate &= IDSRuleFielding.sha256 == ids_fielding.sha256
            query = query.join(IDSRuleFielding, on=(IDSRuleFielding.id == cls.ids_fielding))

        result = query.where(predicate).order_by(cls.num_success.desc()).limit(1)
        if result:
            return result[0]

    @classmethod
    def best_against_cs_fielding(cls, cs_fielding):
        """Get best PoV test results for the provided cs fielding.

        :param cs_fielding: CS fielding for which PoVTestResult need to be fetched.
        :return: List containing best PoV test result.
        """
        query = cls.select(cls).join(ChallengeSetFielding)
        predicate = ChallengeSetFielding.sha256 == cs_fielding.sha256
        result = query.where(predicate).order_by(cls.num_success.desc()).limit(1)
        if result:
            return result[0]

    @classmethod
    def best_against_cs(cls, cs):
        """Get best PoV test results for the provided cs .

        :param cs: CS for which best PoVTestResult need to be fetched.
        :return: List containing best PoV test result.
        """
        query = cls.select(cls).join(ChallengeSetFielding)
        predicate = ChallengeSetFielding.cs == cs
        result = query.where(predicate).order_by(cls.num_success.desc()).limit(1)
        if result:
            return result[0]

    @classmethod
    def best_exploit_test_results(cls, exploit, cs_fielding, ids_fielding):
        """Get results for the provided exploit on cs_fielding and ids_fielding

        :param exploit: Exploit for which results needs to be fetched.
        :param cs_fielding: CS fielding for which PoV testing results need to be fetched.
        :param ids_fielding: IDS fielding for which PoV testing results need to be fetched.
        :return: List of PoVTestResult objects
        """
        query = cls.select(cls).join(ChallengeSetFielding)
        predicate = (ChallengeSetFielding.sha256 == cs_fielding.sha256) \
                    & (PovTestResult.exploit == exploit)

        if ids_fielding is None:
            predicate &= cls.ids_fielding.is_null(True)
        else:
            predicate &= IDSRuleFielding.sha256 == ids_fielding.sha256
            query = query.join(IDSRuleFielding, on=(IDSRuleFielding.id == cls.ids_fielding))

        result = query.where(predicate).order_by(cls.num_success.desc())
        if result:
            return result[0]
