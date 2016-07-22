#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BlobField, BooleanField, ForeignKeyField

from .base import BaseModel
from .challenge_set import ChallengeSet

"""Tracer Cache model"""


class TracerCache(BaseModel):
    """TracerCache model"""
    cs = ForeignKeyField(ChallengeSet, related_name='tracer_cache')
    blob = BlobField(null=False)
    concrete_flag = BooleanField(null=False)
