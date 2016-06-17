"""IDSRule model"""

from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_set import ChallengeSet
from .round import Round

class IDSRule(BaseModel):
    """IDSRule model"""
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='ids_rules')
    rules = TextField()
    submitted_at = DateTimeField(null=True)

    def submit(self):
        """Save submission timestamp"""
        self.submitted_at = datetime.now()
        self.save()

    @property
    def submissions(self):
        """Return list of submissions"""
        if self.submitted_at is not None:
            round_ = Round.at_timestamp(self.submitted_at)
            return [{
                'id': self.id,
                'round': round_.num,
                'name': self.rules[:80],
                'submitted_at': str(self.submitted_at),
            }]
        else:
            return []
