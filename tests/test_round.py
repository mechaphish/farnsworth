from nose.tools import *

from . import setup_each, teardown_each
from farnsworth.models import Round

class TestRound:
    def setup(self): setup_each()
    def teardown(self): teardown_each()

    def test_current_round(self):
        Round.create(num=0)
        Round.create(num=1)
        Round.create(num=2)
        assert_equals(Round.current_round().num, 2)
