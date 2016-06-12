"""RawRoundTraffic model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import BlobField
from .round import Round
from .base import BaseModel


class RawRoundTraffic(BaseModel):
    """
    Result corresponding to the network dude
    """
    round = ForeignKeyField(Round, related_name='raw_round_traffics')
    pickled_data = BlobField()
