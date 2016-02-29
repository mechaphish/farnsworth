# -*- coding: utf-8 -*-

__authors__ = "Francesco Disperati"
__version__ = "0.0.0"


from .. import app, postgres
from flask import request
from utils import jsonify, filter_query, update_query
from datetime import datetime
import psycopg2

@app.route("/bitmaps")
@jsonify
def list_bitmaps():
    cursor = postgres.cursor()

    filterable_cols = ['id', 'cbn_id', 'created_at', 'updated_at']
    query = """SELECT id, created_at, updated_at, cbn_id, blob FROM bitmaps"""
    cursor.execute(*filter_query(query, filterable_cols, request.args))

    return cursor.fetchall()


@app.route("/bitmaps/<int:bitmap_id>")
@jsonify
def get_bitmap(bitmap_id):
    cursor = postgres.cursor()
    cursor.execute("""SELECT * FROM bitmaps WHERE id = %s""", [bitmap_id])
    result = cursor.fetchone()
    if result:
        return result
    else:
        return {'errors': ['not found']}, 404

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
