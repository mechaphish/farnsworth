#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from peewee import CharField, IntegerField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .round import Round

import cPickle as pickle

"""ChallengeSet model"""


class ChallengeSet(BaseModel):
    """ChallengeSet model"""
    name = CharField()
    rounds = ManyToManyField(Round, related_name='cs')

    def seen_in_round(self, round_):
        """Wrap manytomany.add() to add round without duplicates"""
        if round_ not in self.rounds:
            self.rounds.add(round_)

    @classmethod
    def fielded_in_round(cls, round_=None):
        """Return all CS that are fielded in specified round.

        Args:
          round_: Round model instance. If none last round is used.
        """
        if round_ is None:
            round_ = Round.current_round()
        tm = cls.rounds.get_through_model()
        return cls.select().join(tm).where(tm.round == round_)

    def submit(self, cbns=[], round=None):
        """Save patches submission at specified round. If none use current."""
        from .challenge_set_fielding import ChallengeSetFielding
        from .team import Team
        if round is None:
            round = Round.current_round()
        return ChallengeSetFielding.create(cs=self,
                                           cbns=cbns,
                                           submission_round=round,
                                           team=Team.get_our())
    @property
    def unsubmitted_ids_rules(self):
        """Return IDS rules not submitted"""
        from .ids_rule import IDSRule
        from .ids_rule_fielding import IDSRuleFielding
        IDSRF = IDSRuleFielding
        idsr_submitted_ids = [idsrf.ids_rule_id for idsrf in IDSRF.all()]
        if not idsr_submitted_ids:
            return self.ids_rules
        else:
            return self.ids_rules.where(IDSRule.id.not_in(idsr_submitted_ids))

    @property
    def unsubmitted_exploits(self):
        """Return exploits not submitted"""
        from .exploit import Exploit
        from .exploit_fielding import ExploitFielding
        from .challenge_binary_node import ChallengeBinaryNode
        exp_fielding_ids = [expf.exploit_id for expf in ExploitFielding.all()]
        if not exp_fielding_ids:
            return self.exploits
        else:
            return self.exploits.where(Exploit.id.not_in(exp_fielding_ids))

    def _feedback(self, name):
        from .feedback import Feedback
        for fb in Feedback.all():
            for cs in getattr(fb, name):
                if cs['csid'] == self.name:
                    cs['round'] = fb.round.num
                    cs['updated_at'] = str(fb.updated_at)
                    yield cs

    def feedback_polls(self):
        return list(self._feedback('polls'))

    def feedback_cbs(self):
        return list(self._feedback('cbs'))

    def feedback_povs(self):
        return list(self._feedback('povs'))

    def cbns_by_patch_type(self):
        """
        Return all patched CBNs grouped by patch_type.
        """
        from .challenge_binary_node import ChallengeBinaryNode
        groups = {}
        for cbn in self.cbns.where(ChallengeBinaryNode.patch_type.is_null(False)):
            groups.setdefault(cbn.patch_type, []).append(cbn)
        return groups

    @property
    def cbns_original(self):
        """
        Return all original CBNs in this challenge set.
        """
        from .challenge_binary_node import ChallengeBinaryNode
        from .challenge_set_fielding import ChallengeSetFielding
        from .round import Round
        from .team import Team
        # original CBs are CBs by our team available in the first round of this CS
        CSF = ChallengeSetFielding
        first_fielding = self.fieldings\
                             .where(CSF.team == Team.get_our())\
                             .join(Round,
                                   on=(Round.id == ChallengeSetFielding.available_round))\
                             .order_by(Round.num).get()
        return first_fielding.cbns

    @property
    def is_multi_cbn(self):
        return len(self.cbns_original) > 1

    @property
    def fuzzer_stat(self):
        """Return fuzzer stats"""
        if not self.fuzzer_stats_collection:
            return None
        return self.fuzzer_stats_collection[0]

    @property
    def completed_caching(self):
        """Has the cache job on this binary completed"""
        from .job import Job
        return Job.select().where((Job.cs == self) &\
                (Job.worker == 'cache') &\
                (Job.completed_at.is_null(False))).exists()

    @property
    def undrilled_tests(self):
        """Return all undrilled test cases."""
        from .test import Test
        return self.tests.where(Test.drilled == False)

    @property
    def symbols(self):
        symbols = dict()
        from .function_identity import FunctionIdentity
        for function in self.function_identities.where(FunctionIdentity.symbol.is_null(False)).select():
            symbols[function.address] = function.symbol
        return symbols

    @property
    def func_infos(self):
        finfos = dict()
        for function in self.function_identities:
            finfos[function.address] = pickle.loads(function.func_info)

        return finfos

    @property
    def found_crash(self):
        return self.crashes.exists()

    def _has_type(self, typename):
        from .exploit import Exploit
        return self.exploits.where((Exploit.pov_type == typename)\
                & (Exploit.reliability > 0)).exists()

    @property
    def has_type1(self):
        return self._has_type('type1')

    @property
    def has_type2(self):
        return self._has_type('type2')

    @property
    def has_circumstantial_type2(self):
        from .exploit import Exploit
        return self.exploits.where((Exploit.pov_type == 'type2') \
                                   & (Exploit.reliability > 0) \
                                   & (Exploit.method == 'circumstantial')).exists()

    def unprocessed_submission_cables(self):
        """Return all unprocessed cables order by creation date descending."""
        from .cs_submission_cable import CSSubmissionCable
        return self.submission_cables\
            .select()\
            .where(CSSubmissionCable.processed_at.is_null(True))\
            .order_by(CSSubmissionCable.created_at)

    def has_submissions_in_round(self, round):
        """Return True if it has a submission for our team in specified round"""
        from .challenge_set_fielding import ChallengeSetFielding
        from .team import Team
        return self.fieldings\
                   .where((ChallengeSetFielding.submission_round == round) & \
                          (ChallengeSetFielding.team == Team.get_our()))\
                   .exists()
