from peewee import *
import os

db = PostgresqlDatabase(
    os.environ['POSTGRES_DATABASE_NAME'],
    user=os.environ['POSTGRES_DATABASE_USER'],
    password=os.environ['POSTGRES_DATABASE_PASSWORD'],
    host=os.environ['POSTGRES_SERVICE_HOST'],
    port=os.environ['POSTGRES_SERVICE_PORT'],
)
