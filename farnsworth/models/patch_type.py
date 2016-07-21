#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import CharField, FloatField

from .base import BaseModel

"""patch_type_config model"""


class APatchType(BaseModel):
    """
    Patch Types
    """
    name = CharField(null=False)
    functionality_risk = FloatField(null=False)
    exploitability = FloatField(null=False)
