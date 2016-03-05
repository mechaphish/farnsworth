import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

from farnsworth import *
from farnsworth.config import db

# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

def truncate_tables():
    tables = [
        Bitmap,
        ChallengeBinaryNode,
        Crash,
        Exploit,
        Job,
        Pcap,
        Performance,
        Round,
        Score,
        Team,
        Test,
    ]
    table_names = map(lambda t: t._meta.db_table, tables)
    db.execute_sql("TRUNCATE {} RESTART IDENTITY CASCADE".format(", ".join(table_names)))