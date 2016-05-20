"""Base model class"""

from datetime import datetime
from peewee import Model, DateTimeField
from playhouse.read_slave import ReadSlaveModel

from ..config import master_db, slave_db
from ..utils import table_name

if slave_db is not None:
    BaseClass = ReadSlaveModel
else:
    BaseClass = Model

class BaseModel(BaseClass):
    """Base model class"""
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:                 # pylint:disable=old-style-class,no-init,too-few-public-methods,missing-docstring
        database = master_db
        read_slaves = (slave_db,)
        db_table_func = table_name
        validate_backrefs = False # bugfix https://github.com/coleifer/peewee/issues/465

    @classmethod
    def find(cls, id_):
        """Get record by id"""
        try:
            return cls.get(cls.id == id_) # pylint:disable=no-member
        except cls.DoesNotExist:          # pylint:disable=no-member
            return None

    @classmethod
    def find_or_create(cls, **kwargs):
        """Find or create record by attributes"""
        conditions = [
            getattr(cls, attr) == value
            for attr, value in kwargs.items()
        ]
        try:
            return cls.get(*conditions)
        except cls.DoesNotExist: # pylint:disable=no-member
            return cls.create(**kwargs)

    @classmethod
    def all(cls):
        """Return all record sorted by id"""
        return cls.select().order_by(cls.id.asc())

    def save(self, **kwargs):
        self.updated_at = datetime.now()
        return super(BaseModel, self).save(**kwargs)
