from peewee import *

from .base import BaseModel

class Team(BaseModel):
    name = CharField()
