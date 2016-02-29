from peewee import *

from .base import BaseModel

class ChallengeBinaryNode(BaseModel):
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self', to_field='id')
    blob = BlobField(null=True)
    name = CharField()
    root = ForeignKeyField(db_column='root_id', null=True, rel_model='self', to_field='id', related_name='challenge_binary_nodes_root_set')
    # parent_path = UnknownField(null=True)  # FIXMEx
