# -*- coding: utf-8 -*-

__authors__ = "Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from utils import jsonify, filter_query


@app.route("/bitmaps", methods=['POST'])
@jsonify
def create_bitmap():
    d = request.get_json()

    cursor = postgres.cursor()
    cursor.execute("""INSERT INTO bitmaps
    (cbn_id, blob)
    VALUES (%s, %s)
    RETURNING *""",
                   (d['cbn_id'], d['blob']))

    if cursor.rowcount == 0:
        return {"errors": []}, 422
    else:
        return cursor.fetchone(), 201
