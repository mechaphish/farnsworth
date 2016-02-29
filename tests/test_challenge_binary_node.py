from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

from nose.tools import *

from farnsworth import *

class TestAllFixme:
    def test_relationship(self):
        cbn = ChallengeBinaryNode.create(name = "test")
        job = Job.create(worker = "afl", cbn = cbn)
        assert_equals(job.cbn.id, cbn.id)
