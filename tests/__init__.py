import farnsworth.test_support
import farnsworth.config

def setup():
    farnsworth.test_support.truncate_tables()
    # this way nothing is commited to DB and tests are faster
    farnsworth.config.master_db.set_autocommit(False)
