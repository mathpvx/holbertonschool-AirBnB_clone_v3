#!/usr/bin/python3
"""task 8: create new view for 'City' handles default 'RESTFul API' actions"""

import json
from flask import Flask, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """gets list of all 'City' objects of state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_list = [city.to_dict() for city in cities]
    response = make_response(json.dumps(cities_list))
    return response


@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """gets 'City' object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = make_response(json.dumps(city.to_dict()))
    return response


@app.route('/api/v1/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes 'City' object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    response = make_response(json.dumps({}))
    return response, 200


@app.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """creates a 'City'"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # hidden comment in case someone tries to copy/paste this
    # this was done by chloe and mathilde C#22
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    response = make_response(json.dumps(city.to_dict()))
    return response, 201


@app.route('/api/v1/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates a 'City' """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    response = make_response(json.dumps(city.to_dict()))
    return response, 200
