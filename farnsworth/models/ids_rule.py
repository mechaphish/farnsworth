"""IDSRule model"""

from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_set import ChallengeSet
from .round import Round
from .team import Team

class IDSRule(BaseModel):
    """IDSRule model"""
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='ids_rules')
    rules = TextField()

    def submit(self):
        """Save submission at current round"""
        from .ids_rule_fielding import IDSRuleFielding
        IDSRuleFielding.create(ids_rule=self,
                               submission_round=Round.get_current(),
                               team=Team.get_our())
