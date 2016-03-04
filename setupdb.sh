#!/usr/bin/env bash

[ -f .env ] && source .env

drop()
{
    echo [*] dropdb -U $POSTGRES_DATABASE_USER -h $POSTGRES_SERVICE_HOST -p $POSTGRES_SERVICE_PORT --if-exists $POSTGRES_DATABASE_NAME
    dropdb -U $POSTGRES_DATABASE_USER -h $POSTGRES_SERVICE_HOST -p $POSTGRES_SERVICE_PORT --if-exists $POSTGRES_DATABASE_NAME
}

create()
{
    echo [*] createdb -U $POSTGRES_DATABASE_USER -h $POSTGRES_SERVICE_HOST -p $POSTGRES_SERVICE_PORT $POSTGRES_DATABASE_NAME
    createdb -U $POSTGRES_DATABASE_USER -h $POSTGRES_SERVICE_HOST -p $POSTGRES_SERVICE_PORT $POSTGRES_DATABASE_NAME
    echo [*] psql -U $POSTGRES_DATABASE_USER -h $POSTGRES_SERVICE_HOST -p $POSTGRES_SERVICE_PORT $POSTGRES_DATABASE_NAME < support/database/schema.sql
    psql -U $POSTGRES_DATABASE_USER -h $POSTGRES_SERVICE_HOST -p $POSTGRES_SERVICE_PORT $POSTGRES_DATABASE_NAME < support/database/schema.sql
}

case "$1" in
    drop)
        drop
        ;;
    create)
        create
        ;;
    *)
        drop
        create
        ;;
esac
