from peewee import *

from .base import BaseModel

class Team(BaseModel):
    name = CharField()

    @classmethod
    def find_or_create(cls, name):
        try:
            return cls.get(cls.name == name)
        except cls.DoesNotExist:
            return cls.create(name=name)

    @classmethod
    def opponents(cls):
        return cls.select().where(cls.name != "6")
