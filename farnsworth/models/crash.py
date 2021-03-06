#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import BigIntegerField, BlobField, BooleanField, FixedCharField, ForeignKeyField
from ..peewee_extensions import EnumField

from .base import BaseModel
from .challenge_set import ChallengeSet
from .concerns.indexed_blob_model import IndexedBlobModel
from .job import Job

"""Crash model module."""

class Crash(IndexedBlobModel, BaseModel): # Inherited classes order matters!
    blob = BlobField(null=True)
    cs = ForeignKeyField(ChallengeSet, related_name='crashes')
    exploited = BooleanField(default=False)
    explored = BooleanField(default=False)
    job = ForeignKeyField(Job, related_name='crashes')
    triaged = BooleanField(null=False, default=False)
    kind = EnumField(choices=['unclassified',
                              'unknown',
                              'ip_overwrite',
                              'partial_ip_overwrite',
                              'uncontrolled_ip_overwrite',
                              'bp_overwrite',
                              'partial_bp_overwrite',
                              'write_what_where',
                              'write_x_where',
                              'uncontrolled_write',
                              'arbitrary_read',
                              'null_dereference',
                              'arbitrary_transmit',
                              'arbitrary_receive'],
                     enum_name='enum_crash_kind',
                     default='unclassified',
                     null=True)
    crash_pc = BigIntegerField(null=True) # pc at the time of the crash
    bb_count = BigIntegerField(null=True) # basic block count
    sha256 = FixedCharField(max_length=64)

    class Meta:     # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'crashes'
