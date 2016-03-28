from peewee import *
from playhouse.postgres_ext import JSONField
import json

from .base import BaseModel
from .round import Round
from .team import Team
from .round_related_model import RoundRelatedModel

class Evaluation(BaseModel, RoundRelatedModel):
    round = ForeignKeyField(Round, related_name='feedbacks')
    team = ForeignKeyField(Team, related_name='feedbacks')
    ids = JSONField()
    cbs =  JSONField()
