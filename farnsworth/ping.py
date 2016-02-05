#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"


from . import app
from utils import jsonify


@app.route("/ping")
@jsonify
def ping():
    return {"status": "pong"}
