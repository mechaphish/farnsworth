from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from .base import BaseModel

import os

class ChallengeBinaryNode(BaseModel):
    parent = ForeignKeyField('self', related_name='children')
    root = ForeignKeyField('self', related_name='descendants')
    blob = BlobField(null=True)
    name = CharField()
    cs_id = CharField()
    # parent_path = UnknownField(null=True)  # FIXMEx

    @property
    def path(self):
        return os.path.join(os.path.dirname(__file__), '../../../cbs', os.environ['CGC_EVENT'], self.cs_id, self.name)

    @property
    def undrilled_tests(self):
        from .test import Test
        return self.tests.where(Test.drilled == False)
