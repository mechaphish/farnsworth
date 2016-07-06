"""cb_poll_performances model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import JSONField
from .base import BaseModel
from .valid_polls import ValidPoll
from .challenge_set import ChallengeSet


class CbPollPerformance(BaseModel):
    """
    Performance of a CB against a poll.
    """
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='cb_poll_performances')
    poll = ForeignKeyField(ValidPoll, db_column='poll_id', related_name='cb_poll_performances')
    performances = JSONField()
    is_poll_ok = BooleanField()
    patch_type = CharField()
