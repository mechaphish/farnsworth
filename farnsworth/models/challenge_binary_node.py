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
    # needed for submitting patch+related ids rules
    ids_rule = ForeignKeyField(IDSRule, related_name='cbn', null=True)
    # needed for patch submission decision making.
    is_blacklisted = BooleanField(default=False)

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
        return self.descendants \
                   .join(tm, on=(tm.challengebinarynode == ChallengeBinaryNode.id)) \
                   .join(ChallengeSetFielding) \
                   .where(
                       (ChallengeSetFielding.team == Team.get_our()) &
                       (ChallengeSetFielding.submission_round.is_null(False)))

    @property
    def estimated_feedback(self):
        try:
            return PatchScore.get((PatchScore.cs == self.cs)
                                  & (PatchScore.patch_type == self.patch_type))
        except PatchScore.DoesNotExist:
            return None

    @property
    def estimated_cb_score(self):
        if self.estimated_feedback is not None:
            return self.estimated_feedback.cb_score
        else:
            return None

    @property
    def poll_feedbacks(self):
        """All the received polls for this CB."""
        # There is probably a DB way to do this better
        from .challenge_set_fielding import ChallengeSetFielding as CSF
        from .poll_feedback import PollFeedback as PF
        total = (PF.success + PF.timeout + PF.connect + PF.function)
        query = self.fieldings.select(CSF.poll_feedback) \
                              .join(PF, on=(CSF.poll_feedback == PF.id)) \
                              .where((CSF.team == Team.get_our())
                                     & (CSF.poll_feedback.is_null(False))
                                     & (total > 0))
        return [csf.poll_feedback for csf in query]

    @property
    def min_cb_score(self):
        try:
            return min(f.cb_score for f in self.poll_feedbacks)
        except ValueError:
            # No feedbacks available, arg to min is None
            return None

    @property
    def avg_cb_score(self):
        try:
            return _avg(f.cb_score for f in self.poll_feedbacks)
        except ValueError:
            # No feedbacks available, arg to _avg is None
            return None

    @classmethod
    def roots(cls):
        """Return all root nodes (original CB)"""
        return cls.select().where(cls.root.is_null(True))

    @classmethod
    def all_descendants(cls):
        """Return all descendant nodes (patches)"""
        return cls.select().where(cls.root.is_null(False))
