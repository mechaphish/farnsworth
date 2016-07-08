from peewee import *
from .test import Test
from .challenge_set import ChallengeSet
from .round import Round
from .base import BaseModel
import os


class ValidPoll(BaseModel):
    """
        Result corresponding to the TesterJob
    """
    test = ForeignKeyField(Test, db_column='test_id', to_field='id', related_name='valid_polls')
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='valid_polls')
    round = ForeignKeyField(Round, related_name='valid_polls')
    is_perf_ready = BooleanField(null=False)
    has_scores_computed = BooleanField(null=False)
    blob = BlobField()

    @property
    def _path(self):
        """Return path name"""
        filename = "{}-{}".format(self.id, self.cbn.id)
        return os.path.join(os.path.expanduser("~"), filename + '.xml')

    @property
    def path(self):
        """Save poll blob to file and return path"""
        if not os.path.isfile(self._path):
            fp = open(self._path, 'wb')
            fp.write(self.blob)
            fp.close()
        return self._path
