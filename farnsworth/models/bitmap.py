#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BlobField, ForeignKeyField

from .base import BaseModel
from .challenge_set import ChallengeSet

"""Bitmap model"""


class Bitmap(BaseModel):
    """Bitmap model"""
    cs = ForeignKeyField(ChallengeSet, related_name='bitmap')
    blob = BlobField(null=True)
