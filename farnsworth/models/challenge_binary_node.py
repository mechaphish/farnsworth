from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from .base import BaseModel

import os

class ChallengeBinaryNode(BaseModel):
    parent = ForeignKeyField('self', related_name='children')
    root = ForeignKeyField('self', related_name='descendants')
    blob = BlobField()
    name = CharField()
    cs_id = CharField()
    # parent_path = UnknownField(null=True)  # FIXME

    @property
    def path(self):
        return os.path.join(os.environ['CGC_CBS_PATH'], self.cs_id, self.name)

    @property
    def undrilled_tests(self):
        from .test import Test
        return self.tests.where(Test.drilled == False)
