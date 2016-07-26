#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import hashlib
from peewee import CharField, BlobField, ForeignKeyField, FixedCharField, BooleanField, IntegerField

from .base import BaseModel
from .challenge_set import ChallengeSet
from .ids_rule import IDSRule
from .patch_type import PatchType
from .patch_score import PatchScore
from .team import Team
# Imports for Exploit, Round, Exploit deferred to prevent circular imports.


def _sha256sum(*strings):
    array = list(strings)
    array.sort()
    return hashlib.sha256("".join(array)).hexdigest()


def _avg(xs):
    count, sum_ = 0, 0
    for x in xs:
        sum_ += x
        count += 1

    if count > 0:
        return sum_ / count
    else:
        raise ValueError("_avg() arg is an empty sequence")


class ChallengeBinaryNode(BaseModel):
    """ChallengeBinaryNode model"""
    root = ForeignKeyField('self', null=True, related_name='descendants')
    blob = BlobField()
    name = CharField()
    size = IntegerField()
    cs = ForeignKeyField(ChallengeSet, related_name='cbns')
    sha256 = FixedCharField(max_length=64)
    patch_type = ForeignKeyField(PatchType, related_name='patched_cbns', null=True)
    ids_rule = ForeignKeyField(IDSRule, related_name='cbn', null=True) # needed for submitting patch+related ids rules

    is_blacklisted = BooleanField(default=False)  # needed for patch submission decision making.

    def delete_binary(self):
        """Remove binary file"""
        if os.path.isfile(self._path):
            os.remove(self._path)

    @classmethod
    def create(cls, *args, **kwargs):
        kwargs['size'] = len(kwargs['blob'])
        if 'sha256' not in kwargs:
            kwargs['sha256'] = _sha256sum(kwargs['blob'])
        obj = super(cls, cls).create(*args, **kwargs)
        return obj

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

    #
    # Feedback crap
    #

    @property
    def estimated_feedback(self):
        try:
            return PatchScore.select().where(
                (PatchScore.cs == self.cs) &
                (PatchScore.patch_type == self.patch_type)
            ).get()
        except PatchScore.DoesNotExist:
            return None

    @property
    def estimated_cb_score(self):
        return self.estimated_feedback.cb_score if self.estimated_feedback is not None else None

    @property
    def poll_feedbacks(self):
        """All the received polls for this CB."""
        # there is probably a DB way to do this better
        return [
            f.poll_feedback for f in self.fieldings.where(CSF.team == Team.get_our())
            if f.poll_feedback is not None and (
                f.poll_feedback.success + f.poll_feedback.timeout +
                f.poll_feedback.connect + f.poll_feedback.function
            )> 0
        ]

    @property
    def min_cb_score(self):
        feedbacks = self.poll_feedbacks
        return min(f.cb_score for f in feedbacks) if len(feedbacks) else None

    @property
    def avg_cb_score(self):
        try:
            return _avg(f.cb_score for f in self.poll_feedbacks)
        except ValueError:
            # No feedbacks avaiable, arg to _avg is None
            return None

    @classmethod
    def roots(cls):
        """Return all root nodes (original CB)"""
        return cls.select().where(cls.root.is_null(True))

    @classmethod
    def all_descendants(cls):
        """Return all descendant nodes (patches)"""
        return cls.select().where(cls.root.is_null(False))

from .challenge_set_fielding import ChallengeSetFielding as CSF
