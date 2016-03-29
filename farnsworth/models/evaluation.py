from peewee import *
from playhouse.postgres_ext import JSONField
import json
from datetime import datetime

from .base import BaseModel
from .round import Round
from .team import Team

class Evaluation(BaseModel):
    round = ForeignKeyField(Round, related_name='feedbacks')
    team = ForeignKeyField(Team, related_name='feedbacks')
    ids = JSONField()
    cbs =  JSONField()

    @classmethod
    def update_or_create(cls, round_, team, **kwargs):
        update = cls.update(updated_at=datetime.now(),
                            **kwargs).where(cls.round == round_,
                                            cls.team == team)
        if update.execute() == 0:
            cls.create(round=round_, team=team, **kwargs)
