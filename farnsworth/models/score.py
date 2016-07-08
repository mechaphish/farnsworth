"""Score model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel
from .round import Round
from .round_related_model import RoundRelatedModel

class Score(BaseModel, RoundRelatedModel):
    """Score model"""
    round = ForeignKeyField(Round, related_name='scores')
    scores = BinaryJSONField()
    # score_actual = FloatField()
    # score_predicted = FloatField()
