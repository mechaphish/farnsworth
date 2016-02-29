from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from .base import BaseModel

import os

class ChallengeBinaryNode(BaseModel):
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self', to_field='id')
    blob = BlobField(null=True)
    name = CharField()
    cs_id = CharField()
    root = ForeignKeyField(db_column='root_id', null=True, rel_model='self', to_field='id', related_name='challenge_binary_nodes_root_set')
    # parent_path = UnknownField(null=True)  # FIXMEx

    @property
    def path(self):
        os.path.join(__file__, '../../../cbs', os.environ['CGC_EVENT'], self.cs_id, self.name)
