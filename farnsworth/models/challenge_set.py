"""ChallengeSet model"""

import os
from datetime import datetime
from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import

from .base import BaseModel

class ChallengeSet(BaseModel):
    """ChallengeSet model"""
    name = CharField()
