# Farnsworth

Farnsworth is the knowledge base of the Shellphish CRS.
It provides a collection of models to access the PostgreSQL data store.


## Requirements

* Postgresql>=9.5


## Usage

Set your db connection params in the env of your project (see .env.test).
Then:

```
from farnsworth import *

job = Job.get(1)
```


## Test

```
pip install -r requirements.txt
pip install -e .
cp .env.test .env
# edit .env
./setupdb.sh
nosetests tests
```
