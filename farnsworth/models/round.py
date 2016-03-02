from peewee import *

from .base import BaseModel

class Round(BaseModel):
    ends_at = DateTimeField()
