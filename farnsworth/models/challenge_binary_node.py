# pylint:disable=cyclic-import
"""ChallengeBinaryNode model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_set import ChallengeSet
from .round import Round

class ChallengeBinaryNode(BaseModel):
    """ChallengeBinaryNode model"""
    parent = ForeignKeyField('self', related_name='children')
    root = ForeignKeyField('self', related_name='descendants')
    blob = BlobField()
    name = CharField()
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', to_field='id',
                         related_name='cbns')
    submitted_at = DateTimeField(null=True)
    patch_type = CharField(null=True)
    # parent_path = UnknownField(null=True)  # FIXME

    def __init__(self, *args, **kwargs):
        """Create CS on the fly if cs_id is a string"""
        if isinstance(kwargs.get('cs_id'), basestring):
            kwargs['cs'] = ChallengeSet.find_or_create(name = kwargs['cs_id'])
            del(kwargs['cs_id'])
        super(BaseModel, self).__init__(*args, **kwargs)

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
            fp = open(self._path, 'wb')
            fp.write(self.blob)
            fp.close()
            os.chmod(self._path, 0o777)
        return self._path

    def prefix_path(self, prefix_str=None):
        """
        Returns path of a binary with filename prefixed with a given string.
        :param prefix_str: string to be prefixed for filename
        :return: new path to the binary
        """
        if prefix_str is None:
            return self.path
        new_fname = prefix_str + os.path.basename(self._path)
        prefixed_path = os.path.join(os.path.dirname(self._path), new_fname)
        fp = open(prefixed_path, 'wb')
        fp.write(self.blob)
        fp.close()
        os.chmod(prefixed_path, 0o777)
        return prefixed_path

    @property
    def undrilled_tests(self):
        """Rertun all undrilled test cases"""
        from .test import Test
        return self.tests.where(Test.drilled == False)

    @property
    def not_colorguard_traced(self):
        """Rertun all undrilled test cases"""
        from .test import Test
        return self.tests.where(Test.colorguard_traced == False)

    @property
    def found_crash(self):
        return bool(len(self.crashes))

    @property
    def unsubmitted_patches(self):
        """Rertun all unsubmitted patches"""
        return self.descendants.where(self.__class__.submitted_at.is_null(True))

    @property
    def submitted_patches(self):
        """Rertun all submitted patches"""
        return self.descendants.where(self.__class__.submitted_at.is_null(False))

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

    @property
    def submissions(self):
        """Return list of submissions"""
        if self.submitted_at is not None:
            round_ = Round.at_timestamp(self.submitted_at)
            return [{
                'id': self.id,
                'round': round_.num,
                'name': self.name,
                'submitted_at': str(self.submitted_at),
            }]
        else:
            return []
