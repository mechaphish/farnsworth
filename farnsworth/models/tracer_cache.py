#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BlobField, ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

"""Tracer Cache model"""


class TracerCache(BaseModel):
    """TracerCache model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id',
                          related_name='tracer_cache')
    blob = BlobField(null=False)
