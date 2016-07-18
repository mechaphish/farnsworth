#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import CharField, BigIntegerField, ForeignKeyField, BlobField

from .base import BaseModel
from .challenge_set import ChallengeSet

""" Function Identity model """


class FunctionIdentity(BaseModel):
    """ Function Identity model """
    cs = ForeignKeyField(ChallengeSet, related_name='function_identities')
    address = BigIntegerField(null=False)
    symbol = CharField(null=True)
    func_info = BlobField(null=True)

    class Meta:  # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'function_identities'
