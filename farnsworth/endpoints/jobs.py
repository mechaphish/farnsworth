#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = "Kevin Borgolte, Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from datetime import datetime
from utils import jsonify, filter_query, update_query
import psycopg2


@app.route("/jobs")
@jsonify
def list_jobs():
    cursor = postgres.cursor()

    filterable_cols = ['id', 'worker', 'priority', 'cbn_id',
                       'started_at', 'completed_at']

    query = """SELECT id, worker, priority, created_at, started_at,
                      completed_at, cbn_id, limit_cpu, limit_memory,
                      payload, produced_output
                 FROM jobs"""

    cursor.execute(*filter_query(query, filterable_cols, request.args))

    return cursor.fetchall()


@app.route("/jobs/<int:job_id>")
@jsonify
def get_job(job_id):
    cursor = postgres.cursor()
    cursor.execute("""SELECT * FROM jobs WHERE id = %s""", [job_id])
    return cursor.fetchone()


@app.route("/jobs", methods=['POST'])
@jsonify
def create_job():
    d = request.get_json()
    cursor = postgres.cursor()
    cursor.execute("""INSERT INTO jobs
    (worker, limit_cpu, limit_memory, cbn_id, payload)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *""",
                   (d['worker'], d['limit_cpu'], d['limit_memory'],
                    d['cbn_id'], psycopg2.Binary(str(d['payload']))))

    if cursor.rowcount == 0:
        return {"errors": []}
    else:
        return cursor.fetchone()


@app.route("/jobs/<int:job_id>", methods=["PUT"])
@jsonify
def update_job(job_id):
    cursor = postgres.cursor()

    job = request.get_json()
    job.update({
        'payload': psycopg2.Binary(str(job['payload'])),
        'updated_at': datetime.now()
    })
    where = {'id': job_id}
    cursor.execute(*update_query('jobs', job, where))
    cursor.execute("""SELECT * FROM jobs WHERE id = %s""", [job_id])

    if cursor.rowcount == 0:
        return {"errors": []}
    else:
        return cursor.fetchone()
