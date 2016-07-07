"""Tracer Cache model"""

from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class TracerCache(BaseModel):
    """TracerCache model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='tracer_cache')
    blob = BlobField()

    class Meta: # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'tracer_caches'

