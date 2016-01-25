#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The database is the central point for all other parts of the CTF framework.
It is a HTTP REST interface that sits between the actual MySQL database and
the other components. It allows all other components to report on the state of
the game or query the state of the game.

The database API follows some basic design guidelines:
- Every endpoint that only retrieves data but does not add or modify anything is a GET request.
- Every endpoint that adds to the state of the database is a POST request.
- Every endpoint that updates the state of the database is a PUT request.
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"


from . import app
from utils import jsonify


@app.route("/ping")
@jsonify
def general_ping():
    """The ``/ping`` endpoint can be used to check if the API is reachable
    and if it is alive.

    The Json response looks like::

        {"status": "pong"}

    :return: a JSON dictionary with a simple status
    """
    return {"status": "pong"}
