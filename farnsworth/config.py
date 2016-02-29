from peewee import *
from os import environ as ENV

db = PostgresqlDatabase(
    ENV['POSTGRES_DATABASE_NAME'],
    user=ENV['POSTGRES_DATABASE_USER'],
    password=ENV['POSTGRES_DATABASE_PASSWORD'],
    host=ENV['POSTGRES_SERVICE_HOST'],
    port=ENV['POSTGRES_SERVICE_PORT'],
)

# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())
