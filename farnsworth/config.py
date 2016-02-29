from peewee import *
import os
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

db = PostgresqlDatabase(
    os.environ['POSTGRES_DATABASE_NAME'],
    user=os.environ['POSTGRES_DATABASE_USER'],
    password=os.environ['POSTGRES_DATABASE_PASSWORD'],
    host=os.environ['POSTGRES_SERVICE_HOST'],
    port=os.environ['POSTGRES_SERVICE_PORT'],
)

# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())
