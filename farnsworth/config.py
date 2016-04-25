from playhouse.postgres_ext import PostgresqlExtDatabase # for JSONB type
import os

master_db = PostgresqlExtDatabase(
    os.environ['POSTGRES_DATABASE_NAME'],
    user=os.environ['POSTGRES_DATABASE_USER'],
    password=os.environ['POSTGRES_DATABASE_PASSWORD'],
    host=os.environ['POSTGRES_MASTER_SERVICE_HOST'],
    port=os.environ['POSTGRES_MASTER_SERVICE_PORT'],
    register_hstore=False,
    autocommit=True,
    autorollback=True,
)

if os.environ.get('POSTGRES_USE_SLAVES') is not None:
    slave_db = PostgresqlExtDatabase(
        os.environ['POSTGRES_DATABASE_NAME'],
        user=os.environ['POSTGRES_DATABASE_USER'],
        password=os.environ['POSTGRES_DATABASE_PASSWORD'],
        host=os.environ['POSTGRES_SLAVE_SERVICE_HOST'],
        port=os.environ['POSTGRES_SLAVE_SERVICE_PORT'],
        register_hstore=False,
    )
else:
    slave_db = None

def connect_dbs():
    for db in (master_db, slave_db):
        if db is not None:
            db.connect()

def close_dbs():
    for db in (master_db, slave_db):
        if db is not None and not db.is_closed():
            db.close()
