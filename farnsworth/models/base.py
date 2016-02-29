from peewee import *
from datetime import datetime

from ..config import db
from ..utils import table_name

class BaseModel(Model):
    id = BigIntegerField(primary_key=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        db_table_func = table_name
