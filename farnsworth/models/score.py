from peewee import *
from playhouse.postgres_ext import JSONField
import json

from .base import BaseModel
from .round import Round
from .round_related_model import RoundRelatedModel

class Score(BaseModel, RoundRelatedModel):
    round = ForeignKeyField(Round, related_name='scores')
    scores = JSONField()
    # score_actual = FloatField()
    # score_predicted = FloatField()
