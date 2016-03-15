from peewee import *
from playhouse.postgres_ext import JSONField
import json

from .base import BaseModel
from .round import Round

class Feedback(BaseModel):
    round = ForeignKeyField(Round, related_name='feedbacks')
    polls = JSONField()
    cbs =  JSONField()
    povs = JSONField()
