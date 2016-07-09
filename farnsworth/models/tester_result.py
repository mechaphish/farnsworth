#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField, IntegerField, CharField, TextField
from playhouse.postgres_ext import BinaryJSONField

from .job import Job
from .base import BaseModel

"""TesterResult model"""


class TesterResult(BaseModel):
    """
    Result corresponding to the TesterJob
    """
    job = ForeignKeyField(Job, db_column='job_id',  related_name='tester_results')
    error_code = IntegerField()
    performances = BinaryJSONField()
    result = CharField()
    stdout_out = TextField()
    stderr_out = TextField()
