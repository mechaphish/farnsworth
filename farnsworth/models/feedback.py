from peewee import *
from playhouse.postgres_ext import JSONField
import json

from .base import BaseModel
from .round import Round
from .round_related_model import RoundRelatedModel

class Feedback(BaseModel, RoundRelatedModel):
    round = ForeignKeyField(Round, related_name='feedbacks')
    polls = JSONField()
    cbs =  JSONField()
    povs = JSONField()
