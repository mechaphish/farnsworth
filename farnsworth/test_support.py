"""Test helper module."""

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env.test') # pylint: disable=invalid-name
load_dotenv(dotenv_path)

from farnsworth.models import * # pylint:disable=wildcard-import,unused-wildcard-import
from farnsworth.config import master_db

# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

def truncate_tables():
    """Truncate all tables"""
    tables = [
        Bitmap,
        ChallengeBinaryNode,
        ChallengeSet,
        Crash,
        Evaluation,
        Exploit,
        Feedback,
        FuzzerStat,
        IDSRule,
        Job,
        Pcap,
        Round,
        Score,
        Team,
        Test,
        TesterResult,
    ]
    table_names = map(lambda t: t._meta.db_table, tables) # pylint:disable=protected-access,deprecated-lambda,bad-builtin
    master_db.execute_sql("TRUNCATE {} RESTART IDENTITY CASCADE".format(", ".join(table_names)))
