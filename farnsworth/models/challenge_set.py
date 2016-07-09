#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from peewee import CharField, IntegerField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .round import Round

"""ChallengeSet model"""


class ChallengeSet(BaseModel):
    """ChallengeSet model"""
    name = CharField()
    rounds = ManyToManyField(Round, related_name='cs')

    @classmethod
    def fielded_in_round(cls, round_=None):
        """Return all CS that are fielded in specified round.

        Args:
          round_: Round model instance. If none last round is used.
        """
        if round_ is None:
            round_ = Round.get_current()
        return cls.select().where(cls.rounds.contains_any(round_.id))

    @property
    def unsubmitted_ids_rules(self):
        """Return IDS rules not submitted"""
        from .ids_rule import IDSRule
        from .ids_rule_fielding import IDSRuleFielding
        IDSRF = IDSRuleFielding
        idsr_submitted_ids = [idsrf.ids_rule_id for idsrf in IDSRF.all()]
        if len(idsr_submitted_ids) == 0:
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
        if len(exp_fielding_ids) == 0:
            return Exploit.select().join(ChallengeBinaryNode).where(
                ChallengeBinaryNode.cs == self)
        else:
            return Exploit.select().join(ChallengeBinaryNode).where(
                (ChallengeBinaryNode.cs == self) &
                Exploit.id.not_in(exp_fielding_ids))

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
    def cbns_unpatched(self):
        """
        Return all unpatched CBNs in a list.
        """
        from .challenge_binary_node import ChallengeBinaryNode
        # FIXME: we are storing other teams' binaries with '-' in the filename,
        # skip this files
        return self.cbns.where(
            ChallengeBinaryNode.patch_type.is_null(True) & ~(ChallengeBinaryNode.name ** "%-%"))
