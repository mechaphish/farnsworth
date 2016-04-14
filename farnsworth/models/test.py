from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .job import Job

class Test(BaseModel):
    blob = BlobField()
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='tests')
    job = ForeignKeyField(Job, db_column='job_id', to_field='id', related_name='tests')
    drilled = BooleanField()

    @classmethod
    def unsynced_testcases(cls, worker, prev_sync_time):
        return cls.select().where(cls.job.worker == worker & cls.created_at > prev_sync_time)
