#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = "Kevin Borgolte, Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from utils import jsonify, filter_query, update_query


@app.route("/crashes")
@jsonify
def list_crashes():
    cursor = postgres.cursor()

    filterable_cols = [
        'id', 'cbn_id', 'job_id', 'triaged', 'explored',
        'exploited', 'explorable', 'exploitable'
    ]
    query = ""

    if 'with_descendants' in request.args:
        query = """SELECT t.id, t.cbn_id, t.job_id, t.triaged, t.explored,
                          t.exploited, t.explorable, t.exploitable,
                          t.created_at, t.updated_at,
                          encode(t.blob, 'base64') as blob
                   FROM crashes AS t, challenge_binary_nodes AS cbns
                   WHERE t.cbn_id = cbns.id
                   AND cbns.parent_path ~ %s"""
        path_query = '*.%s.*' % request.args['cbn_id']
        cursor.execute(query, [path_query])
    else:
        query = """SELECT id, cbn_id, job_id, triaged,
                          explored, explorable, exploitable, exploited
                          created_at, updated_at,
                          encode(blob, 'base64') as blob
                          FROM crashes"""
        cursor.execute(*filter_query(query, filterable_cols, request.args))

    return cursor.fetchall()


@app.route("/crashes/<int:crash_id>")
@jsonify
def get_crash(crash_id):
    cursor = postgres.cursor()
    cursor.execute("""SELECT * FROM crashes WHERE id = %s""", [crash_id])
    resource = cursor.fetchone()
    if resource:
        return resource
    else:
        return {'errors': ['not found']}, 404


@app.route("/crashes", methods=["POST"])
@jsonify
def create_crash():
    cursor = postgres.cursor()

    crash = request.get_json()
    cursor.execute("""INSERT INTO crashes (cbn_id, job_id, triaged, explored, explored, explorable, exploitable, exploited, blob)
                      VALUES (%(cbn_id)s, %(job_id)s, %(triaged)s, %(explored)s, %(explorable)s, %(exploited)s, %(exploitable)s, decode(%(blob)s, 'base64'))
                      RETURNING id, cbn_id, job_id, triaged, explored, explorable, exploited, exploitable, encode(blob, 'base64') as blob, created_at, updated_at""",
                   crash)

    if cursor.rowcount == 0:
        return {"errors": []}, 422
    else:
        return cursor.fetchone(), 201


@app.route("/crashes/<int:crash_id>", methods=["PUT"])
@jsonify
def update_crash(crash_id):
    cursor = postgres.cursor()

    crash = request.get_json()
    cursor.execute(*update_query('crashes', updates, where))

    if cursor.rowcount == 0:
        return {"errors": []}, 422
    else:
        return cursor.fetchone()
