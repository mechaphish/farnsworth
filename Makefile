docker-postgres:
	docker run -p 127.0.0.1:5432:5432 --name postgres -t -d postgres

develop:
	@export FARNSWORTH_DB_SETTINGS=`pwd`/develop.settings
	python develop.py
