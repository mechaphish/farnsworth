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
from farnsworth.models.job import AFLJob

job = AFLJob.get(1)
```

Please note that importing any models directly from `farnsworth.models` is deprecated. Instead,
you should be importing them explicitly by specifying the module they are contained in.

Finally, please read [Peewee documentation](https://peewee.readthedocs.org/en/latest/peewee/querying.html)
to see how you can query the database.


### Use with multi-process

You need to open a new db connection for every process.
To do so:

```
import farnsworth.config

farnsworth.config.connect_dbs()
Job.create(...)
farnsworth.config.close_dbs()
```


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
