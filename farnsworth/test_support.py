import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env.test')
load_dotenv(dotenv_path)

from farnsworth.models import *
from farnsworth.config import master_db

# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

def truncate_tables():
    tables = [
        Bitmap,
        ChallengeBinaryNode,
        Crash,
        Evaluation,
        Exploit,
        Feedback,
        FuzzerStat,
        Job,
        Pcap,
        Round,
        Score,
        Team,
        Test,
    ]
    table_names = map(lambda t: t._meta.db_table, tables)
    master_db.execute_sql("TRUNCATE {} RESTART IDENTITY CASCADE".format(", ".join(table_names)))
