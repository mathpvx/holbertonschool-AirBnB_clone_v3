#!/usr/bin/python3
"""
Task 8: Create new view for 'City' that handles default 'RESTFul API' actions
"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Get all cities of a state.
    """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    json_format = []
    for city in the_state.cities:
        json_format.append(city.to_dict())
    return jsonify(json_format)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_cities_withId(city_id):
    """Get city with a provided ID.
    """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    else:
        return jsonify(the_city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object if found.
    """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    else:
        storage.delete(the_city)
        storage.save()
        return {}, 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city.
    """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)

    http_body_request = request.get_json(silent=True)
    if http_body_request is None:
        return "Not a JSON\n", 400
    elif "name" not in http_body_request:
        return "Missing name\n", 400
    else:
        new_city = City(name=http_body_request["name"], state_id=state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a given city.
    """
    the_city = storage.get(City, city_id)
    ignore_keys_list = ["id", "created_at", "updated_at", "state_id"]
    if the_city is None:
        abort(404)
    else:
        http_body_request = request.get_json(silent=True)
        if http_body_request is None:
            return "Not a JSON\n", 400
        else:
            for key, value in http_body_request.items():
                if key not in ignore_keys_list:
                    setattr(the_city, key, value)
        storage.save()
        return jsonify(the_city.to_dict()), 200
