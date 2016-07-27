#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Rop Cache model"""

from __future__ import absolute_import, unicode_literals

from peewee import BlobField, ForeignKeyField

from .base import BaseModel
from .challenge_set import ChallengeSet


class RopCache(BaseModel):
    """RopCache model"""
    cs = ForeignKeyField(ChallengeSet, related_name='rop_cache')
    blob = BlobField(null=False)
