from peewee import *

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .job import Job

class Test(BaseModel):
    blob = BlobField(null=True)
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode, to_field='id')
    job = ForeignKeyField(db_column='job_id', rel_model=Job, to_field='id')
    drilled = BooleanField()
