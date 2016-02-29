from peewee import *

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class Bitmap(BaseModel):
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNode, to_field='id', related_name='bitmap')
    blob = BlobField(null=True)
