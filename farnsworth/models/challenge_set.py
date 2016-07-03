#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os

from peewee import CharField
from playhouse.postgres_ext import ArrayField

from .base import BaseModel
from .feedback import Feedback
from .round import Round

"""ChallengeSet model"""


class ChallengeSet(BaseModel):
    """ChallengeSet model"""
    name = CharField()
    rounds = ArrayField(IntegerField)

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
        return self.ids_rules.where(IDSRule.submitted_at.is_null(True))

    def _feedback(self, name):
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
