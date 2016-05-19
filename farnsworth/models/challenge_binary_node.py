# pylint:disable=cyclic-import
"""ChallengeBinaryNode model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class ChallengeBinaryNode(BaseModel):
    """ChallengeBinaryNode model"""
    parent = ForeignKeyField('self', related_name='children')
    root = ForeignKeyField('self', related_name='descendants')
    blob = BlobField()
    name = CharField()
    cs_id = CharField()
    submitted_at = DateTimeField(null=True)
    # parent_path = UnknownField(null=True)  # FIXME

    def delete_binary(self):
        """Remove binary file"""
        if os.path.isfile(self._path):
            os.remove(self._path)

    def __del__(self):
        self.delete_binary()

    def submit(self):
        """Save submission timestamp"""
        self.submitted_at = datetime.now()
        self.save()

    @property
    def fuzzer_stat(self):
        """Return fuzzer stats"""
        if len(self.fuzzer_stats_collection) == 0:
            return None
        return self.fuzzer_stats_collection[0]

    @property
    def _path(self):
        """Return path name"""
        filename = "{}-{}-{}".format(self.id, self.cs_id, self.name)
        return os.path.join(os.path.expanduser("~"), filename) # FIXME: afl doesn't like /tmp

    @property
    def path(self):
        """Save binary blob to file and return path"""
        if not os.path.isfile(self._path):
            open(self._path, 'wb').write(self.blob)
            os.chmod(self._path, 0o777)
        return self._path

    @property
    def undrilled_tests(self):
        """Rertun all undrilled test cases"""
        from .test import Test
        return self.tests.where(Test.drilled is False)

    @property
    def unsubmitted_patches(self):
        """Rertun all unsubmitted patches"""
        return self.descendants.where(self.__class__.submitted_at.is_null(True))

    @property
    def unsubmitted_exploits(self):
        """Return exploits not submitted"""
        from .exploit import Exploit
        return self.exploits.where(Exploit.submitted_at.is_null(True))

    @property
    def all_tests_for_this_cb(self):
        """Return all tests for this CB and its descendants"""
        from .test import Test
        return Test.select().where(Test.cbn == self.root)

    @classmethod
    def roots(cls):
        """Return all root nodes (original CB)"""
        return cls.select().where(cls.root.is_null(True))

    @classmethod
    def all_descendants(cls):
        """Return all descendant nodes (patches)"""
        return cls.select().where(cls.root.is_null(False))
