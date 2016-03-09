from peewee import Model, DateTimeField
from playhouse.read_slave import ReadSlaveModel
from datetime import datetime

from ..config import master_db, slave_db
from ..utils import table_name

if slave_db is not None:
    base_class = ReadSlaveModel
else:
    base_class = Model

class BaseModel(base_class):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = master_db
        read_slaves = (slave_db,)
        db_table_func = table_name
        validate_backrefs = False # bugfix https://github.com/coleifer/peewee/issues/465

    @classmethod
    def find(cls, id):
        try:
            return cls.get(cls.id == id)
        except cls.DoesNotExist:
            return None
