#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = "Kevin Borgolte, Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from utils import jsonify, filter_query, update_query


@app.route("/tests")
@jsonify
def list_tests():
    cursor = postgres.cursor()

    filterable_cols = ['id', 'cbn_id', 'job_id', 'type']
    query = ""

    if 'with_descendants' in request.args:
        query = """SELECT t.id, t.cbn_id, t.job_id, t.type,
                          t.created_at, t.updated_at,
                          encode(t.blob, 'base64') as blob
                   FROM tests AS t, challenge_binary_nodes AS cbns
                   WHERE t.cbn_id = cbns.id
                   AND cbns.parent_path ~ %s"""
        path_query = '*.%s.*' % request.args['cbn_id']
        cursor.execute(query, [path_query])
    else:
        query = """SELECT id, cbn_id, job_id, type,
                          created_at, updated_at,
                          encode(blob, 'base64') as blob
                          FROM tests"""
        cursor.execute(*filter_query(query, filterable_cols, request.args))

    return cursor.fetchall()


@app.route("/tests/<int:test_id>")
@jsonify
def get_test(test_id):
    cursor = postgres.cursor()
    cursor.execute("""SELECT * FROM tests WHERE id = %s""", [test_id])
    return cursor.fetchone()


@app.route("/tests", methods=["POST"])
@jsonify
def create_test():
    cursor = postgres.cursor()

    test = request.get_json()
    cursor.execute("""INSERT INTO tests (cbn_id, job_id, type, blob)
                      VALUES (%(cbn_id)s, %(job_id)s, %(type)s, decode(%(blob)s, 'base64'))
                      RETURNING id, cbn_id, job_id, type, encode(blob, 'base64') as blob, created_at, updated_at""",
                   test)

    if cursor.rowcount == 0:
        return {"errors": []}
    else:
        return cursor.fetchone()


@app.route("/tests/<int:test_id>", methods=["PUT"])
@jsonify
def update_test(test_id):
    cursor = postgres.cursor()

    test = request.get_json()
    cursor.execute(*update_query('tests', updates, where))

    if cursor.rowcount == 0:
        return {"errors": []}
    else:
        return cursor.fetchone()
