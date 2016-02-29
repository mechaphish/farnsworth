# -*- coding: utf-8 -*-

__authors__ = "Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from utils import jsonify, update_query
from datetime import datetime
import psycopg2


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

@app.route("/bitmaps/<int:bitmap_id>", methods=["PUT"])
@jsonify
def update_bitmap(bitmap_id):
    cursor = postgres.cursor()

    bitmap = request.get_json()
    bitmap.update({
        'blob': psycopg2.Binary(str(bitmap['blob'])),
        'updated_at': datetime.now()
    })
    where = {'id': bitmap_id}
    cursor.execute(*update_query('bitmaps', bitmap, where))
    cursor.execute("""SELECT * FROM bitmaps WHERE id = %s""", [bitmap_id])

    if cursor.rowcount == 0:
        return {"errors": []}, 422
    else:
        return cursor.fetchone()
