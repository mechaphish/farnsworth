#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Jobs Endpoint
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"


from . import app, postgres
from utils import jsonify


@app.route("/jobs")
@jsonify
def jobs_status():
    """The ``/jobs`` endpoint can be used to check if the API is reachable
    and if it is alive.

    The JSON response looks like::

        [{"id": <numerical id>,
          "worker": <string identifier of the worker>,
          "priority": <integer> (higher value = higher priority),
          "created_at": <timestamp>,
          "started_at": <timestamp>,
          "completed_at": <timestamp>,
          "ctn_id": <id of the challenge tree node>,
          "limit_cpu": <maximum number of cores>,
          "limit_memory": <maximum amount of memory in MB>,
          "produced_output": <true if the job is completed and produced output,
                              false if the job did not produce any output,
                              null if the job has not completed yet>
         }, ...]

    :return: a list of dictionaries as above
    """
    cursor = postgres.cursor()

    cursor.execute("""SELECT id, worker, priority, created_at, started_at,
                             completed_at, ctn_id, limit_cpu, limit_memory,
                             produced_output
                      FROM jobs""")

    return cursor.fetchall()
