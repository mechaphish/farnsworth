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

```
pip install -r requirements.txt
dropdb --if-exists DBNAME
createdb -U nebirhos farnsworth_test
psql DBNAME -U DBUSER < support/database/schema.sql
```

## Test

```
cp .env.development .env.test
# create test db
# edit .env.test
nosetests tests
```
