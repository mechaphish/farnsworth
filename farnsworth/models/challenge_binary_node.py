#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

"""ChallengeBinaryNode model"""

import os
from datetime import datetime

from peewee import CharField, BlobField, DateTimeField, ForeignKeyField

from .base import BaseModel
from .challenge_set import ChallengeSet
from .round import Round
# Imports for Test and Exploit deferred to prevent circular imports.


class ChallengeBinaryNode(BaseModel):
    """ChallengeBinaryNode model"""
    root = ForeignKeyField('self', null=True, related_name='descendants')
    blob = BlobField(null=True)
    name = CharField()
    cs = ForeignKeyField(ChallengeSet, db_column='cs_id', related_name='cbns')
    patch_type = CharField(null=True)

    def delete_binary(self):
        """Remove binary file"""
        if os.path.isfile(self._path):
            os.remove(self._path)

    def __del__(self):
        self.delete_binary()

    @property
    def fuzzer_stat(self):
        """Return fuzzer stats"""
        if not self.fuzzer_stats_collection:
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
            with open(self._path, 'wb') as fp:
                fp.write(self.blob)
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
        with open(prefixed_path, 'wb') as fb:
            fp.write(self.blob)
        os.chmod(prefixed_path, 0o777)
        return prefixed_path

    @property
    def undrilled_tests(self):
        """Return all undrilled test cases."""
        from .test import Test
        return self.tests.where(Test.drilled == False)

    @property
    def not_colorguard_traced(self):
        """Return all undrilled test cases."""
        from .test import Test
        return self.tests.where(Test.colorguard_traced == False)

    def submit(self):
        """Save submission at current round"""
        from .challenge_binary_node_fielding import ChallengeBinaryNodeFielding
        from .team import Team
        ChallengeBinaryNodeFielding.create(cbn=self,
                                           submission_round=Round.get_current(),
                                           team=Team.get_our())

    @property
    def symbols(self):
        symbols = dict()
        for function in self.function_identities.select():
            symbols[function.address] = function.symbol

        return symbols

    @property
    def found_crash(self):
        return bool(len(self.crashes))

    @property
    def completed_caching(self):
        """Has the cache job on this binary completed"""
        from .job import Job
        return Job.select().where((Job.cbn == self) &\
                (Job.worker == 'cache') &\
                (Job.completed_at.is_null(False))).exists()

    @property
    def unsubmitted_patches(self):
        """Rertun all unsubmitted patches"""
        from .challenge_binary_node_fielding import ChallengeBinaryNodeFielding
        CBNF = ChallengeBinaryNodeFielding
        cbn_submitted_ids = [cbnf.cbn_id for cbnf in CBNF.all()]
        if len(cbn_submitted_ids) == 0:
            return self.descendants
        else:
            return self.descendants.where(self.__class__.id.not_in(cbn_submitted_ids))

    @property
    def submitted_patches(self):
        """Rertun all submitted patches"""
        from .challenge_binary_node_fielding import ChallengeBinaryNodeFielding
        from .team import Team
        CBNF = ChallengeBinaryNodeFielding
        return self.descendants.join(CBNF).where(
            CBNF.submission_round.is_null(False) & (CBNF.team == Team.get_our())
        )

    # FIXME
    @property
    def unsubmitted_exploits(self):
        """Return exploits not submitted"""
        from .exploit import Exploit    # Preventing circular import
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
