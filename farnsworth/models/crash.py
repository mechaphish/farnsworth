#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Crash model module."""

# pylint: disable=missing-docstring

from peewee import BlobField, BooleanField, ForeignKeyField
from ..peewee_extensions import EnumField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .job import Job

class Crash(BaseModel):
    blob = BlobField(null=True)
    cbn = ForeignKeyField(db_column='cbn_id',
                          rel_model=ChallengeBinaryNode,
                          to_field='id',
                          related_name='crashes')
    exploitable = BooleanField(null=True)
    exploited = BooleanField(null=True)
    explorable = BooleanField(null=True)
    explored = BooleanField(null=True)
    job = ForeignKeyField(db_column='job_id',
                          rel_model=Job,
                          to_field='id',
                          related_name='crashes')
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
                              'null_dereference'],
                     default='unclassified',
                     null=False)

    class Meta:     # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'crashes'

# pylint: enable=missing-docstring
