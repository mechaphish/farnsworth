# -*- coding: utf-8 -*-

__authors__ = "Francesco Disperati"
__version__ = "0.0.0"


from . import app, postgres
from flask import request
from datetime import datetime
from utils import jsonify, filter_query


@app.route("/cbns", methods=['POST'])
@jsonify
def create_challenge_binary_node():
    d = request.get_json()

    now = datetime.now().isoformat()
    cursor = postgres.cursor()
    cursor.execute("""INSERT INTO challenge_binary_nodes
    (root_id, parent_id, parent_path, name, blob, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id""",
                   (None, None, None,
                    d['name'], d['blob'], now))

    if cursor.rowcount == 0:
        return {"errors": []}
    else:
        new_record_id = cursor.fetchone()['id']
        return {"id": new_record_id}


@app.route("/cbns", methods=['GET'])
@jsonify
def list_challenge_binary_nodes():
    cursor = postgres.cursor()

    filterable_cols = ['name', 'parent_id']
    cursor.execute(*filter_query("""SELECT * from challenge_binary_nodes""",
                                 filterable_cols, request.args))

    return cursor.fetchall()
