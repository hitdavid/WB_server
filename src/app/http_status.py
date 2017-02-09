# -*- coding: utf-8 -*-
from flask import jsonify

def on_404(e):
    return jsonify(dict(error='Not found')), 404
