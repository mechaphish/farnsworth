#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests Endpoint
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"


from . import app, postgres
from flask import request
from utils import jsonify, filter_query, update_query


@app.route("/tests")
@jsonify
def tests_get():
    """The ``/tests`` endpoint can be used to check if the API is reachable
    and if it is alive.

    The JSON response looks like::

        [{"id": <numerical id>,
          "ctn_id": <id of the challenge tree node>,
          "job_id": <id of the job that created the test, optional>,
          "type": <type of the job>,
          "data": <test data, base64-encoded>
         }, ...]

    :return: a list of dictionaries as above
    """
    cursor = postgres.cursor()

    filterable_cols = ['id', 'ctn_id', 'job_id']

    cursor.execute(*filter_query("""SELECT id, ctn_id, job_id, type,
                                           encode(data, 'base64') as data
                                      FROM tests""",
                                 filterable_cols, request.args))

    return cursor.fetchall()


@app.route("/tests", methods=["POST"])
@jsonify
def tests_post():
    cursor = postgres.cursor(dictionary=False)

    tests = request.get_json()
    if isinstance(tests, dict):
        tests = [tests]

    for test in tests:
        # test['data'] = test['data'].decode('base64')
        print(cursor.mogrify("""INSERT INTO tests (ctn_id, job_id, type, data)
                          VALUES (%(ctn_id)s, %(job_id)s, %(type)s, %(data)s)""", test))

    cursor.executemany("""INSERT INTO tests (ctn_id, job_id, type, data)
                          VALUES (%(ctn_id)s, %(job_id)s, %(type)s, %(data)s)""",
                       tuple(tests))

    return {"status": "added"}  # FIXME should check if added


@app.route("/tests", methods=["PUT"])
@jsonify
def tests_put():
    cursor = postgres.cursor(dictionary=False)

    tests = request.get_json()
    if isinstance(tests, dict):
        tests = [tests]

    for test in tests:
        where = {'id': test['id']}
        updates = test
        del updates['id']

        cursor.execute(*update_query('tests', updates, where))

    return {"status": "updated"}  # FIXME should check if added
