#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"

from farnsworth import app
app.run(debug=True, use_reloader=True, host=app.config['LISTEN'])
