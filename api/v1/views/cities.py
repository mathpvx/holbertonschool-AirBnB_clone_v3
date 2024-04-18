#!/usr/bin/python3
"""task 8: create new view for 'City' handles default 'RESTFul API' actions"""

from flask import abort, request, jsonify
from models import storage
from models.state import State
from models.city import City


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def gets_CitiesState(state_id):
    """gets list of all 'City' objects of state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_list = [city.to_dict() for city in cities]
    return jsonify(cities_list)


@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def gets_city(city_id):
    """gets 'City' object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app.route('/api/v1/cities/<city_id>', methods=['DELETE'])
def deletes_city(city_id):
    """deletes 'City' object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def creates_city(state_id):
    """creates a 'City'"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app.route('/api/v1/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
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
    return jsonify(city.to_dict()), 200
