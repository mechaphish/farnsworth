# Farnsworth

Farnsworth is the knowledge base of the Shellphish CRS. It provides a
JSON-based REST API and uses PostgreSQL as the data store.


## Documentation

API specs follows [API Blueprint](https://apiblueprint.org/) format.

To compile HTML browseable use Aglio:

    npm install -g aglio
    aglio -i doc/api.apib -o doc/index.html

Livereload is also available:

    aglio -i doc/api.apib -o doc/index.html --server
    open http://127.0.0.1:3000/

## Requirements

* Postgresql


## Development

    pip install -r requirements.txt
    psql -U DBUSER < support/database/schema.sql
    mv .env.development .env
    python develop.py

Configurations are managed with environment variables.
Take a look at .env for possible options.
