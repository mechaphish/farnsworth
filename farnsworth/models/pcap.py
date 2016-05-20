"""Pcap model"""

from peewee import * # pylint:disable=wildcard-import,unused-wildcard-import

from ..peewee_extensions import EnumField
from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .round import Round
from .team import Team

class Pcap(BaseModel):
    """Pcap model"""
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='pcaps')
    round = ForeignKeyField(Round, related_name='pcaps')
    team = ForeignKeyField(Team, related_name='pcaps')
    type = EnumField(choices=['unknown', 'test', 'crash', 'exploit'])
