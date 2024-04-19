#!/usr/bin/python3
"""view for Place object that handles all default RESTFul API actions"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """ get all places of a city"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    json_format = []
    for place in the_city.places:
        json_format.append(place.to_dict())
    return jsonify(json_format)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_places_id(place_id):
    """ get place with a provided id"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    else:
        return jsonify(the_place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes a place object"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    else:
        storage.delete(the_place)
        storage.save()
        return {}, 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ creates a place"""

    """Check and get existing city"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    """Check HTTP body request"""
    http_body_request = request.get_json(silent=True)
    if http_body_request is None:
        return "Not a JSON\n", 400
    elif "user_id" not in http_body_request:
        return "Missing user_id\n", 400
    elif "name" not in http_body_request:
        return "Missing name\n", 400
    else:
        """Check user_id"""
        the_user = storage.get(User, http_body_request["user_id"])
        if the_user is None:
            abort(404)
        http_body_request["city_id"] = city_id

        """Create new place"""
        new_place = Place(**http_body_request)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ updates a given place"""
    the_place = storage.get(Place, place_id)
    ignore_keys_list = ["id", "created_at", "updated_at", "city_id", "user_id"]
    if the_place is None:
        abort(404)
    else:
        http_body_request = request.get_json(silent=True)
        if http_body_request is None:
            return "Not a JSON\n", 400
        else:
            for key, value in http_body_request.items():
                if key not in ignore_keys_list:
                    setattr(the_place, key, value)
        storage.save()
        return jsonify(the_place.to_dict()), 200
