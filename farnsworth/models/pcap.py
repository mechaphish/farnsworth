from peewee import *

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .round import Round
from .team import Team

class Pcap(BaseModel):
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='pcaps')
    round = ForeignKeyField(Round, related_name='pcaps')
    team = ForeignKeyField(Team, related_name='pcaps')
    # type = UnknownField()  # USER-DEFINED
