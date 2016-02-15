# -*- coding: utf-8 -*-

__authors__ = "Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from utils import jsonify, filter_query


@app.route("/cbns", methods=['POST'])
@jsonify
def create_challenge_binary_node():
    d = request.get_json()

    cursor = postgres.cursor()
    cursor.execute("""INSERT INTO challenge_binary_nodes
    (root_id, parent_id, parent_path, name, blob)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *""",
                   (None, None, None,
                    d['name'], d['blob']))

    if cursor.rowcount == 0:
        return {"errors": []}, 422
    else:
        return cursor.fetchone(), 201


@app.route("/cbns", methods=['GET'])
@jsonify
def list_challenge_binary_nodes():
    cursor = postgres.cursor()

    filterable_cols = ['name', 'parent_id']
    cursor.execute(*filter_query("""SELECT * FROM challenge_binary_nodes""",
                                 filterable_cols, request.args))
    return cursor.fetchall()

@app.route("/cbns/<int:cbn_id>")
@jsonify
def get_challenge_binary_node(cbn_id):
    cursor = postgres.cursor()
    cursor.execute(
        """SELECT * FROM challenge_binary_nodes WHERE id = %s""", [cbn_id]
    )
    resource = cursor.fetchone()
    if resource:
        return resource
    else:
        return {'errors': ['not found']}, 404
