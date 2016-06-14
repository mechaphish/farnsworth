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
    triaged = BooleanField()
    kind = EnumField(choices=['ip_overwrite', 'arbitrary_read'])

    class Meta:     # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'crashes'

# pylint: enable=missing-docstring
