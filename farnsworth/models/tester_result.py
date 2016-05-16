from peewee import *
from playhouse.postgres_ext import JSONField
from .job import Job
from .base import BaseModel


class TesterResult(BaseModel):
    """
        Result corresponding to the TesterJob
    """
    job = ForeignKeyField(Job, db_column='job_id', to_field='id', related_name='tester_results')
    error_code = IntegerField()
    performances = JSONField()
    result = CharField()
    stdout_out = TextField()
    stderr_out = TextField()
