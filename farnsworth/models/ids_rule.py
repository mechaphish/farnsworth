"""IDSRule model"""

from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_set import ChallengeSet

class IDSRule(BaseModel):
    """IDSRule model"""
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='ids_rules')
    rules = TextField()
    submitted_at = DateTimeField(null=True)

    def submit(self):
        """Save submission timestamp"""
        self.submitted_at = datetime.now()
        self.save()
