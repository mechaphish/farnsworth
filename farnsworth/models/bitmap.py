#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BlobField, ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

"""Bitmap model"""


class Bitmap(BaseModel):
    """Bitmap model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, related_name='bitmap')
    blob = BlobField(null=True)
