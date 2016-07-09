#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from peewee import ForeignKeyField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from ..peewee_extensions import EnumField
from .round import Round
from .team import Team

"""Pcap model"""


class Pcap(BaseModel):
    """PCAP model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='pcaps')
    round = ForeignKeyField(Round, related_name='pcaps')
    team = ForeignKeyField(Team, related_name='pcaps')
    type = EnumField(choices=['unknown', 'test', 'crash', 'exploit'],
                     default='unknown', enum_name='enum_pcap_type')
