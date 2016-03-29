from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from datetime import datetime
import os

from .base import BaseModel

class ChallengeBinaryNode(BaseModel):
    parent = ForeignKeyField('self', related_name='children')
    root = ForeignKeyField('self', related_name='descendants')
    blob = BlobField()
    name = CharField()
    cs_id = CharField()
    submitted_at = DateTimeField(null=True)
    # parent_path = UnknownField(null=True)  # FIXME

    @property
    def path(self):
        filename = "{}-{}-{}".format(self.id, self.cs_id, self.name)
        filepath = os.path.join(os.path.expanduser("~"), filename) # FIXME: afl doesn't like /tmp
        if not os.path.isfile(filepath):
            open(filepath, 'wb').write(self.blob)
            os.chmod(filepath, 0o777)
        return filepath

    @property
    def undrilled_tests(self):
        from .test import Test
        return self.tests.where(Test.drilled == False)

    def __del__(self):
        if os.path.isfile(self.path):
            os.remove(self.path)

    def submitted(self):
        self.submitted_at = datetime.now()
        self.save()

    @property
    def unsubmitted_patches(self):
        return self.children.where(self.__class__.submitted_at.is_null(True))

    @property
    def unsubmitted_exploits(self):
        from .exploit import Exploit
        return self.exploits.where(Exploit.submitted_at.is_null(True))

    @classmethod
    def roots(cls):
        return cls.select().where((cls.parent.is_null(True)))
