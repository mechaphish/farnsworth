#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

__authors__ = "Kevin Borgolte, Francesco Disperati"
__version__ = "0.0.0"

from flask import Flask
from .config import set_config_from_env
from .flaskext.postgresql import PostgreSQL

# Python 3 compatibility
PY3 = sys.version_info[0] == 3

# pylint:disable=invalid-name
if PY3:
    string_types = str,         # pragma: no flakes
    text_type = str             # pragma: no flakes
else:
    string_types = basestring,  # pragma: no flakes
    text_type = unicode         # pragma: no flakes
# pylint:enable=invalid-name


# Initialize Flask
#
# pylint:disable=invalid-name
app = Flask(__name__)
set_config_from_env(app, '.env')

postgres = PostgreSQL(app)
# pylint:enable=invalid-name


# The following files contain subset of the routes
# that are specific to a subset of the functionality
from . import cbns
#from . import cts
from . import jobs
#from . import pcaps
#from . import performances
from . import ping
#from . import scores
#from . import status
#from . import teams
from . import tests

if __name__ == "__main__":
    app.run()
