#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime

from peewee import CharField, BlobField, DateTimeField, ForeignKeyField, FixedCharField, BooleanField

from .base import BaseModel
from .challenge_set import ChallengeSet
from .ids_rule import IDSRule
# Imports for Exploit, Round, Exploit deferred to prevent circular imports.

"""ChallengeBinaryNode model"""


class ChallengeBinaryNode(BaseModel):
    """ChallengeBinaryNode model"""
    root = ForeignKeyField('self', null=True, related_name='descendants')
    blob = BlobField(null=True)
    name = CharField()
    cs = ForeignKeyField(ChallengeSet, related_name='cbns')
    patch_type = CharField(null=True)
    sha256 = FixedCharField(max_length=64)
    ids_rule = ForeignKeyField(IDSRule, related_name='cbn', null=True) # needed for submitting patch+related ids rules
    is_blacklisted = BooleanField(default=False)  # needed for patch submission decision making.

    def delete_binary(self):
        """Remove binary file"""
        if os.path.isfile(self._path):
            os.remove(self._path)

    @property
    def _path(self):
        """Return path name"""
        filename = "{}-{}-{}".format(self.id, self.cs_id, self.name)
        return os.path.join(os.path.expanduser("~"), filename)  # FIXME: afl doesn't like /tmp

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
        with open(prefixed_path, 'wb') as fp:
            fp.write(self.blob)
        os.chmod(prefixed_path, 0o777)
        return prefixed_path

    @property
    def unsubmitted_patches(self):
        """All unsubmitted patches."""
        from .challenge_set_fielding import ChallengeSetFielding
        tm = ChallengeSetFielding.cbns.get_through_model()
        subquery = ChallengeSetFielding.select(tm.challengebinarynode).join(tm)
        return self.descendants.where(self.__class__.id.not_in(subquery))

    @property
    def submitted_patches(self):
        """All submitted patches."""
        from .challenge_set_fielding import ChallengeSetFielding
        from .team import Team
        tm = ChallengeSetFielding.cbns.get_through_model()
        return self.descendants\
                   .join(tm, on=(tm.challengebinarynode == ChallengeBinaryNode.id))\
                   .join(ChallengeSetFielding)\
                   .where(
                       (ChallengeSetFielding.team == Team.get_our()) &
                       (ChallengeSetFielding.submission_round.is_null(False)))

    @classmethod
    def roots(cls):
        """Return all root nodes (original CB)"""
        return cls.select().where(cls.root.is_null(True))

    @classmethod
    def all_descendants(cls):
        """Return all descendant nodes (patches)"""
        return cls.select().where(cls.root.is_null(False))
