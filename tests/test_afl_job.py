from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import AFLJob, RexJob, ChallengeBinaryNode

class TestAFLJob:
    def setup(self):
        setup_each()

    def teardown(self):
        teardown_each()
