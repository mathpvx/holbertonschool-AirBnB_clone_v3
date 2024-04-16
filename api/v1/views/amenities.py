#!/usr/bin/python3
"""A view API for amenities"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Get all amenities"""
    amenities = storage.all(Amenity)
    json_format = []
    for amenity in amenities.values():
        json_format.append(amenity.to_dict())
    return jsonify(json_format)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Get amenity with a provided ID"""
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    else:
        return jsonify(the_amenity.to_dict())


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a amenity"""
    http_body_request = request.get_json(silent=True)
    if http_body_request is None:
        return "Not a JSON\n", 400
    elif "name" not in http_body_request:
        return "Missing name\n", 400
    else:
        new_amenity = Amenity(name=http_body_request["name"])
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a given amenity"""
    the_amenity = storage.get(Amenity, amenity_id)
    ignore_keys_list = ["id", "created_at", "updated_at"]
    if the_amenity is None:
        abort(404)
    else:
        http_body_request = request.get_json(silent=True)
        if http_body_request is None:
            return "Not a JSON\n", 400
        else:
            for key, value in http_body_request.items():
                if key not in ignore_keys_list:
                    setattr(the_amenity, key, value)
        storage.save()
        return jsonify(the_amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity object if found"""
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    else:
        storage.delete(the_amenity)
        storage.save()
        return {}, 200
