from peewee import *

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .job import Job

class Crash(BaseModel):
    blob = BlobField(null=True)
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode, to_field='id')
    exploitable = BooleanField(null=True)
    exploited = BooleanField(null=True)
    explorable = BooleanField(null=True)
    explored = BooleanField(null=True)
    job = ForeignKeyField(db_column='job_id', rel_model=Job, to_field='id')
    triaged = BooleanField()
