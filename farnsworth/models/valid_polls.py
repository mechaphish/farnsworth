from peewee import *
from .test import Test
from .challenge_binary_node import ChallengeBinaryNode
from .round import Round
from .base import BaseModel


class ValidPoll(BaseModel):
    """
        Result corresponding to the TesterJob
    """
    test = ForeignKeyField(Test, db_column='test_id', to_field='id', related_name='valid_polls')
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='valid_polls')
    round = ForeignKeyField(Round, related_name='valid_polls')
    blob = BlobField()
