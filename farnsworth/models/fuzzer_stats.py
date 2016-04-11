from peewee import *

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class FuzzerStats(BaseModel):
    cbn = ForeignKeyField(db_column='cbnid', rel_model=ChallengeBinaryNode, to_field='id', related_name='fuzzer_stats')
    pending_favs = IntegerField(null=True)
    pending_total = IntegerField(null=True)
    paths_total = IntegerField(null=True)
    paths_found = IntegerField(null=True)
    paths_imported = IntegerField(null=True)
    last_path = DateTimeField(null=True)
