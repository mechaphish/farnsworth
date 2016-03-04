from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from playhouse.postgres_ext import JSONField
import json
from datetime import datetime

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class Job(BaseModel):
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', to_field='id', related_name='jobs')
    completed_at = DateTimeField(null=True)
    limit_cpu = IntegerField(null=True)
    limit_memory = IntegerField(null=True)
    limit_time = IntegerField(null=True)
    payload = JSONField()
    priority = IntegerField()
    produced_output = BooleanField(null=True)
    started_at = DateTimeField(null=True)
    worker = CharField()

    class Meta: #pylint:disable=no-init
        db_table_func = lambda x: 'jobs'

    def started(self):
        self.started_at = datetime.now()
        self.save()

    def completed(self):
        self.completed_at = datetime.now()
        self.save()

class DrillerJob(Job):
    '''
    This represents a job for driller. Driller requires a testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    '''

    worker = CharField(default='driller')

    @property
    def input_test(self):
        from .test import Test
        return Test.get(id=self.payload['test_id'])

class AFLJob(Job):
    '''
    This represents a job for AFL. It requires no extra input.
    '''

    worker = CharField(default='afl')

class RexJob(Job):
    '''
    This represents a job for rex. Rex requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    '''

    worker = CharField(default='rex')

    @property
    def input_crash(self):
        from .crash import Crash
        return Crash.get(id=self.payload['crash_id'])
