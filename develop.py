#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper to develop the farnsworth API."""

from farnsworth import app

__authors__ = "Kevin Borgolte <kevin@borgolte.me>"
__version__ = "0.1.0"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host=app.config['LISTEN'])
