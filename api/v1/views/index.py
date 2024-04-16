#!/usr/bin/python3
"""A index file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Return status of the"""
    return jsonify({"status": "OK"})
