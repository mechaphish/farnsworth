from peewee import *

from .base import BaseModel
from .round import Round
from .test import Test

class Score(BaseModel):
    round = ForeignKeyField(Round, related_name='scores')
    test = ForeignKeyField(Test, related_name='scores')
    score_actual = FloatField()
    score_predicted = FloatField()
