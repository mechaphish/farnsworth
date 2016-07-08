"""FuzzerStat model"""

from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode


class FuzzerStat(BaseModel):
    """FuzzerStat model"""
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode,
                          to_field='id', related_name='fuzzer_stats_collection')
    pending_favs = IntegerField(null=False, default=0)
    pending_total = IntegerField(null=False, default=0)
    paths_total = IntegerField(null=False, default=0)
    paths_found = IntegerField(null=False, default=0)
    last_path = DateTimeField(null=True)
