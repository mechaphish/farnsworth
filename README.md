# Farnsworth

Farnsworth is the knowledge base of the Shellphish CRS.
It provides a collection of models to access the PostgreSQL data store.


## Requirements

* Postgresql>=9.5


## Usage

Set your db connection params in the env of your project (see .env.example).
Then:

```
from farnsworth import *

job = Job.get(1)
```


## Test

```
pip install -e .
# edit .env.test if needed
./setupdb.sh .env.test
nosetests tests
```
