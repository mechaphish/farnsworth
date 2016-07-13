#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BlobField, ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

"""Rop Cache model"""


class RopCache(BaseModel):
    """RopCache model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, related_name='rop_cache')
    blob = BlobField(null=False)
