#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import CharField, BigIntegerField, ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

""" Function Identity model """


class FunctionIdentity(BaseModel):
    """ Function Identity model """
    cbn = ForeignKeyField(ChallengeBinaryNode, related_name='function_identities')
    address = BigIntegerField(null=False)
    symbol = CharField(null=False)

    class Meta:  # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'function_identities'
