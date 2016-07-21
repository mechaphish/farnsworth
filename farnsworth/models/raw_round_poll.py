#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BooleanField, BlobField, ForeignKeyField
from playhouse.postgres_ext import BlobField

from ..actions import cfe_poll_from_xml, Write
from .round import Round
from .base import BaseModel
from .challenge_set import ChallengeSet

"""RawRoundPoll model"""


class RawRoundPoll(BaseModel):
    """
    Poll created from network traffic.
    """
    round = ForeignKeyField(Round, related_name='raw_round_polls')
    is_crash = BooleanField(null=False, default=False)
    is_failed = BooleanField(null=False, default=False)
    cs = ForeignKeyField(ChallengeSet, related_name='raw_round_polls')
    blob = BlobField(null=False)
    sanitized = BooleanField(null=False, default=False)

    def from_xml_to_test(self):

        test_blob = [ ]
        for action in cfe_poll_from_xml(str(self.blob)).actions:
            if isinstance(action, Write):
                for data_var in action.data_vars:
                    test_blob.append(data_var.data)

        return ''.join(test_blob)
