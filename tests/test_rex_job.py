from nose.tools import *
from datetime import datetime

from . import setup_each, teardown_each
from farnsworth.models import RexJob, AFLJob, ChallengeBinaryNode, Crash

class TestRexJob:
    def setup(self): setup_each()
    def teardown(self): teardown_each()
