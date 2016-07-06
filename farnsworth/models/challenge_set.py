"""ChallengeSet model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .feedback import Feedback

class ChallengeSet(BaseModel):
    """ChallengeSet model"""
    name = CharField()

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
        Return all CBNs grouped by patch_type.
        """
        from .challenge_binary_node import ChallengeBinaryNode
        groups = {}
        for cbn in self.cbns:
            key = 'original' if cbn.patch_type is None else cbn.patch_type
            groups.setdefault(key, []).append(cbn)
        return groups
