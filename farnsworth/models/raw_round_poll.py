"""RawRoundPoll model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import BlobField
from .round import Round
from .base import BaseModel
from .challenge_set import ChallengeSet


class RawRoundPoll(BaseModel):
    """
    Poll created from network traffic.
    """
    round = ForeignKeyField(Round, related_name='raw_round_polls')
    is_crash = BooleanField()
    is_failed = BooleanField()
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='raw_round_polls')
    blob = BlobField()
