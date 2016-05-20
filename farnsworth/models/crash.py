"""Crash model"""

from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .job import Job

class Crash(BaseModel):
    """Crash model"""
    blob = BlobField(null=True)
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode, to_field='id', related_name='crashes') # pylint:disable=line-too-long
    exploitable = BooleanField(null=True)
    exploited = BooleanField(null=True)
    explorable = BooleanField(null=True)
    explored = BooleanField(null=True)
    job = ForeignKeyField(db_column='job_id', rel_model=Job, to_field='id', related_name='crashes')
    triaged = BooleanField()

    class Meta:                 # pylint:disable=no-init,too-few-public-methods,old-style-class,missing-docstring
        db_table = 'crashes'
