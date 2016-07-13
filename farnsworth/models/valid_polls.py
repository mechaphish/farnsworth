#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from peewee import BooleanField, BlobField, ForeignKeyField

from .test import Test
from .challenge_set import ChallengeSet
from .round import Round
from .base import BaseModel


class ValidPoll(BaseModel):
    """Result corresponding to the TesterJob."""
    test = ForeignKeyField(Test, related_name='valid_polls')
    cs = ForeignKeyField(ChallengeSet, related_name='valid_polls')
    round = ForeignKeyField(Round, related_name='valid_polls', null=True)
    is_perf_ready = BooleanField(null=False, default=True)
    has_scores_computed = BooleanField(null=False, default=False)
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
            with open(self._path, 'wb') as fp:
                fp.write(self.blob)
        return self._path
