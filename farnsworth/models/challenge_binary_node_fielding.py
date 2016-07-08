"""ChallengeBinaryNodeFielding model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .round import Round
from .team import Team

class ChallengeBinaryNodeFielding(BaseModel):
    """ChallengeBinaryNodeFielding model"""

    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id',
                          related_name='fieldings', null=False)
    team = ForeignKeyField(Team, db_column='team_id', to_field='id',
                           related_name='fieldings', null=False)
    submission_round = ForeignKeyField(Round, db_column='submission_round_id',
                                       related_name='fieldings', null=True)
    available_round = ForeignKeyField(Round, db_column='available_round_id',
                                      related_name='fieldings', null=True)
    fielded_round = ForeignKeyField(Round, db_column='fielded_round_id',
                                    related_name='fieldings', null=True)
