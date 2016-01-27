# Farnsworth

Farnsworth is the knowledge base of the Shellphish CRS. It provides a
JSON-based REST API and uses PostgreSQL as the data store.

The PostgreSQL Dockerfiles are stored in support/.


## Requirements

* Postgresql


## Development

    pip install -r requirements.txt
    mv .env.development .env
    python develop.py

Configurations are managed with environment variables.
Take a look at .env for possible options.
