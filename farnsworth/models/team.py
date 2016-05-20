"""Team model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class Team(BaseModel):
    """Team model"""
    name = CharField()

    @classmethod
    def opponents(cls):
        """Return oppenent teams"""
        return cls.select().where(cls.name != "6")
