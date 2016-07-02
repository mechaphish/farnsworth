"""cb_poll_performances model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import BlobField
from .base import BaseModel
from .valid_polls import ValidPoll
from .challenge_binary_node import ChallengeBinaryNode


class CbPollPerformance(BaseModel):
    """
    Performance of a CB against a poll.
    """
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='cb_poll_performances')
    poll = ForeignKeyField(ValidPoll, db_column='poll_id', related_name='cb_poll_performances')
    performances = BlobField()
