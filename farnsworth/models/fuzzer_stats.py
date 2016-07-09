#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import DateTimeField, IntegerField, ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

"""FuzzerStat model"""


class FuzzerStat(BaseModel):
    """FuzzerStat model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, related_name='fuzzer_stats_collection')
    pending_favs = IntegerField(null=False, default=0)
    pending_total = IntegerField(null=False, default=0)
    paths_total = IntegerField(null=False, default=0)
    paths_found = IntegerField(null=False, default=0)
    last_path = DateTimeField(null=True)
