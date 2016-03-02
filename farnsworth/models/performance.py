from peewee import *

from .base import BaseModel
from .test import Test

class Performance(BaseModel):
    test = ForeignKeyField(Test, related_name='performances')
