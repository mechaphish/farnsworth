"""IDSRule model"""

from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class IDSRule(BaseModel):
    """IDSRule model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='ids_rules')
    rules = TextField()
    submitted_at = DateTimeField(null=True)

    def submit(self):
        """Save submission timestamp"""
        self.submitted_at = datetime.now()
        self.save()

    @classmethod
    def unsubmitted(cls):
        """Return unsubmitted IDS rules"""
        return cls.select().where(cls.submitted_at.is_null(True))
