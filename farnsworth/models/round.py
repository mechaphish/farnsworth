"""Round model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class Round(BaseModel):
    """Round model"""
    ends_at = DateTimeField()
    num = IntegerField()
