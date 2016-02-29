# Farnsworth

Farnsworth is the knowledge base of the Shellphish CRS.
It provides a collection of models to access the PostgreSQL data store.


## Requirements

* Postgresql>=9.5


## Usage

Set your db connection params in the env (see .env.development).
Then:

```
from farnsworth import *

job = Job.get(1)
```


## Development

    pip install -r requirements.txt
    psql -U DBUSER < support/database/schema.sql
