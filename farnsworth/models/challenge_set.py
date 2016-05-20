"""ChallengeSet model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class ChallengeSet(BaseModel):
    """ChallengeSet model"""
    name = CharField()

    @property
    def unsubmitted_ids_rules(self):
        """Return IDS rules not submitted"""
        from .ids_rule import IDSRule
        return self.ids_rules.where(IDSRule.submitted_at.is_null(True))
