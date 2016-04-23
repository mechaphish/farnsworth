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

    def is_started(self):
        return self.started_at is not None

    def is_completed(self):
        return self.completed_at is not None

    def completed(self):
        self.completed_at = datetime.now()
        self.save()

    @classmethod
    def unstarted(cls):
        return cls.select().where(cls.started_at.is_null(True) & (cls.worker == cls.worker.default))


class DrillerJob(Job):
    """
    This represents a job for driller. Driller requires a testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='driller')

    def __init__(self, *args, **kwargs):
        self._input_test = None
        super(DrillerJob, self).__init__(*args, **kwargs)

    @property
    def input_test(self):
        from .test import Test
        self._input_test = self._input_test or Test.get(id=self.payload['test_id'])
        return self._input_test

    @classmethod
    def queued(cls, job):
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'driller') &
                    (cls.payload['test_id'] == str(job.payload['test_id'])))
            return True
        except cls.DoesNotExist:
            return False


class AFLJob(Job):
    """
    This represents a job for AFL. It requires no extra input.
    """

    worker = CharField(default='afl')

    @classmethod
    def queued(cls, job):
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'afl') &
                    cls.completed_at.is_null(True))
            return True
        except cls.DoesNotExist:
            return False


class RexJob(Job):
    """
    This represents a job for rex. Rex requires a crashing testcase
    as an input. Here, we receive the testcase as a string in the
    `payload` field.
    """

    worker = CharField(default='rex')

    def __init__(self, *args, **kwargs):
        self._input_crash = None
        super(RexJob, self).__init__(*args, **kwargs)

    @property
    def input_crash(self):
        from .crash import Crash
        self._input_crash = self._input_crash or Crash.get(id=self.payload['crash_id'])
        return self._input_crash

    @classmethod
    def queued(cls, job):
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'rex') &
                    (cls.payload['crash_id'] == str(job.payload['crash_id'])))
            return True
        except cls.DoesNotExist:
            return False


class PatcherexJob(Job):
    worker = CharField(default='patcherex')
    @classmethod
    def queued(cls, job):
        try:
            cls.get((cls.cbn == job.cbn) &
                    (cls.worker == 'patcherex') &
                    cls.completed_at.is_null(True))
            return True
        except cls.DoesNotExist:
            return False


class TesterJob(Job):
    """
    This represents a job for Tester. Tester requires a testcase
    as an input. Here, we receive the testcase id as a string in the
    `payload` field.
    """

    worker = CharField(default='tester')

    def __init__(self, *args, **kwargs):
        self._target_test = None
        super(TesterJob, self).__init__(*args, **kwargs)

    @property
    def target_test(self):
        """
        Get the target test corresponding to this tester job
        :return: Test corresponding to this job.
        """
        from .test import Test
        self._target_test = self._target_test or Test.get(id=self.payload['test_id'])
        return self._target_test

    def mark_job_not_started(self):
        """
        Mark this current job as not started.
        This is required in case, the job incurred an schrodinger failure.
        :return: None
        """
        self.started_at = DateTimeField(null=True)
        self.completed_at = DateTimeField(null=True)
        self.save()




