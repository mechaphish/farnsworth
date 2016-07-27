#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""CSSubmissionCable model"""

from __future__ import absolute_import, unicode_literals

from datetime import datetime

from peewee import DateTimeField, ForeignKeyField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set import ChallengeSet
from .ids_rule import IDSRule
from .round import Round


class CSSubmissionCable(BaseModel):
    """CSSubmissionCable model. Communicate what patch submit to ambassador"""

    cs = ForeignKeyField(ChallengeSet, related_name='submission_cables')
    ids = ForeignKeyField(IDSRule, related_name='submission_cables')
    cbns = ManyToManyField(ChallengeBinaryNode, related_name='submission_cables')
    round = ForeignKeyField(Round, related_name='cs_submission_cables')
    processed_at = DateTimeField(null=True)

    @classmethod
    def create(cls, *args, **kwargs):
        if 'cbns' in kwargs:
            cbns = kwargs.pop('cbns')

        obj = super(cls, cls).create(*args, **kwargs)
        obj.cbns = cbns
        return obj

    @classmethod
    def get_or_create(cls, cs, ids, round, cbns=None):  # pylint: disable=arguments-differ
        if cbns is None:
            cbns = []
        results = cls.select() \
                     .where((cls.cs == cs)
                            & (cls.ids == ids)
                            & (cls.round == round))
        for cssb in results:
            found = {cbn.id for cbn in cssb.cbns}
            expected = {cbn.id for cbn in cbns}
            if (len(found) == len(expected)) and \
               (len(found & expected) == len(expected)):
                return (cssb, False)
        return (cls.create(cs=cs, ids=ids, cbns=cbns, round=round), True)

    def process(self):
        self.processed_at = datetime.now()
        self.save()
