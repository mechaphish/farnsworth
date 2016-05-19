"""Round model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class Round(BaseModel):
    """Round model"""
    ends_at = DateTimeField()
    num = IntegerField()

    @classmethod
    def find_or_create(cls, num):
        """Find or create record"""
        try:
            return cls.get(cls.num == num)
        except cls.DoesNotExist: # pylint:disable=no-member
            return cls.create(num=num)
