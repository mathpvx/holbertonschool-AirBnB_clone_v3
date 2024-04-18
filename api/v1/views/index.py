#!/usr/bin/python3
"""A index file"""


from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Return status of the"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """retrieves the number of each object by type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    obj_count = {}
    for name, cls in classes.items():
        obj_count[name] = storage.count(cls)
    return jsonify(obj_count)
