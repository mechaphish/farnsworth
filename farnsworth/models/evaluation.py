from peewee import *
from playhouse.postgres_ext import JSONField
import json

from .base import BaseModel
from .round import Round
from .team import Team

class Evaluation(BaseModel):
    round = ForeignKeyField(Round, related_name='feedbacks')
    team = ForeignKeyField(Team, related_name='feedbacks')
    ids = JSONField()
    cbs =  JSONField()
