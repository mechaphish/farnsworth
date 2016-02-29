from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class Job(BaseModel):
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode, to_field='id')
    completed_at = DateTimeField(null=True)
    limit_cpu = IntegerField(null=True)
    limit_memory = IntegerField(null=True)
    payload = BlobField(null=True)
    priority = IntegerField()
    produced_output = BooleanField(null=True)
    started_at = DateTimeField(null=True)
    worker = CharField()

    @property
    def completed(self):
        return self.completed is not None

class DrillerJob(Job):
    '''
    This represents a job for driller. Driller requires a testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    '''

    @property
    def input_test(self):
        from .test import Test
        return Test.get(id=self.payload)

    class Meta: #pylint:disable=no-init
        db_table = 'jobs'

class AFLJob(Job):
    '''
    This represents a job for AFL. It requires no extra input.
    '''

    class Meta: #pylint:disable=no-init
        db_table = 'jobs'

class RexJob(Job):
    '''
    This represents a job for rex. Rex requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    '''

    @property
    def input_crash(self):
        from .crash import Crash
        return Crash.get(id=self.payload)

    class Meta: #pylint:disable=no-init
        db_table = 'jobs'

