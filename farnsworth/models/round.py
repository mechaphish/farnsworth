"""Round model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class Round(BaseModel):
    """Round model"""
    ends_at = DateTimeField()
    num = IntegerField()

    @classmethod
    def current_round(cls):
        return cls.select().order_by(cls.created_at.desc())[0]
