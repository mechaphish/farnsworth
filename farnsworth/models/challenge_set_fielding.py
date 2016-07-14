#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import datetime
import os
import hashlib

from peewee import FixedCharField, ForeignKeyField
from playhouse.fields import ManyToManyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .challenge_set import ChallengeSet
from .round import Round
from .team import Team

"""ChallengeSetFielding model"""


def _sha256sum(*strings):
    array = list(strings)
    array.sort()
    return hashlib.sha256("".join(array)).hexdigest()


class ChallengeSetFielding(BaseModel):
    """ChallengeSetFielding model"""

    cs = ForeignKeyField(ChallengeSet, related_name='fieldings')
    team = ForeignKeyField(Team, related_name='cs_fieldings')
    submission_round = ForeignKeyField(Round, related_name='cs_fieldings', null=True)
    available_round = ForeignKeyField(Round, related_name='cs_fieldings', null=True)
    fielded_round = ForeignKeyField(Round, related_name='cs_fieldings', null=True)
    cbns = ManyToManyField(ChallengeBinaryNode, related_name='cbns')
    sha256 = FixedCharField(max_length=64)

    @classmethod
    def create(cls, *args, **kwargs):
        if 'cbns' in kwargs:
            cbns = kwargs.pop('cbns')

        if 'sha256' not in kwargs:
            kwargs['sha256'] = _sha256sum(*[c.sha256 for c in cbns])

        obj = super(cls, cls).create(*args, **kwargs)
        obj.cbns = cbns
        return obj
