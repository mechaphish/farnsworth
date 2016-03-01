from peewee import *
from datetime import datetime

from ..config import db
from ..utils import table_name

class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        db_table_func = table_name

    @classmethod
    def find(cls, id):
        try:
            return cls.get(cls.id == id)
        except cls.DoesNotExist:
            return None
