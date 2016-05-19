"""Feedback model"""

from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import JSONField

from .base import BaseModel
from .round import Round
from .round_related_model import RoundRelatedModel

class Feedback(BaseModel, RoundRelatedModel):
    """Feedback model"""
    round = ForeignKeyField(Round, related_name='feedbacks')
    polls = JSONField()
    cbs = JSONField()
    povs = JSONField()
