#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import hashlib
import os

from peewee import DateTimeField, ForeignKeyField, IntegerField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set import ChallengeSet
from .ids_rule import IDSRule

"""ChallengeSetSubmissionCable model"""


class ChallengeSetSubmissionCable(BaseModel):
    """ChallengeSetSubmissionCable model. Communicate what patch submit to ambassador"""

    cs = ForeignKeyField(ChallengeSet, related_name='submission_cables')
    ids = ForeignKeyField(IDSRule, related_name='submission_cables')
    # FIXME: make it multi-cb
    cbns = ForeignKeyField(ChallengeBinaryNode, related_name='submission_cables')
    processed_at = DateTimeField(null=True)

    @classmethod
    def unprocessed(cls):
        """Return all unprocessed cables order by creation date descending."""
        return cls.select()\
                  .where(cls.processed_at.is_null(True))\
                  .order_by(cls.created_at.desc())

    def process(self):
        self.processed_at = datetime.now()
        self.save()
