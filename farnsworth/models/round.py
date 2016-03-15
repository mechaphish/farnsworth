from peewee import *

from .base import BaseModel

class Round(BaseModel):
    ends_at = DateTimeField()
    num = IntegerField()

    @classmethod
    def find_or_create(cls, num):
        try:
            return cls.get(cls.num == num)
        except cls.DoesNotExist:
            return cls.create(num=num)
