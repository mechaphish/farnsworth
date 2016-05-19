"""Team model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class Team(BaseModel):
    """Team model"""
    name = CharField()

    @classmethod
    def find_or_create(cls, name):
        """Find or create record"""
        try:
            return cls.get(cls.name == name)
        except cls.DoesNotExist: # pylint:disable=no-member
            return cls.create(name=name)

    @classmethod
    def opponents(cls):
        """Return oppenent teams"""
        return cls.select().where(cls.name != "6")
