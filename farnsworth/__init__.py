#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

"""Farnsworth is the central knowledge database for the Shellphish CRS.

It is a HTTP REST interface that sits between the actual PostgreSQL database, the meister, and the
actual workers.  It allows all other components to report on the state of the game or query the
state of the game.

The database API follows some basic design guidelines:
- Every endpoint that only retrieves data but does not add or modify anything is a GET request.
- Every endpoint that adds to the state of the database is a POST request.
- Every endpoint that updates the state of the database is a PUT request.
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"

from flask import Flask
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


# Initialize Flask and MySQL wrapper
#
# pylint:disable=invalid-name
app = Flask(__name__)
app.config.from_envvar("FARNSWORTH_DB_SETTINGS")

postgres = PostgreSQL(app)
# pylint:enable=invalid-name


# The following files contain subset of the routes
# that are specific to a subset of the functionality
#from . import cbs
#from . import cts
#from . import jobs
#from . import pcaps
#from . import performances
from . import ping
#from . import scores
#from . import status
#from . import teams
#from . import tests

if __name__ == "__main__":
    app.run()
