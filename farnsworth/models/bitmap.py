"""Bitmap model"""

from peewee import *            # pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class Bitmap(BaseModel):
    """Bitmap model"""
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode, to_field='id', related_name='bitmap') # pylint:disable=line-too-long
    blob = BlobField(null=True)
