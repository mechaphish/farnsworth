# Farnsworth

Farnsworth is the knowledge base of the Shellphish CRS.
It provides a collection of models to access the PostgreSQL data store.


## Requirements

* Postgresql>=9.5


## Usage

Database params are read from environment variables (see .env.example).

You can set the environment manually, or load a .env file:

```
from dotenv import load_dotenv
load_dotenv('.env')
```

Then:

```
from farnsworth.models import *

job = Job.get(1)
```

Please read [Peewee documentation](https://peewee.readthedocs.org/en/latest/peewee/querying.html)
to see how you can query the db.


## Test

```
pip install -e .
# edit .env.test if needed
./setupdb.sh .env.test
nosetests tests
```


## Guidelines

* simple queries (like `Job.get(worker='afl')`) can stay in your code
* complex queries (`join` and multiple `where`) should stay in the model class
* write at least 1 test case for every method you add
