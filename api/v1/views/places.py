#!/usr/bin/python3
"""task 13: new view for 'Place' objects handles default RESTFul API actions"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_city_places(city_id):
    """retrieve/gets list of 'Place' objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    localisation = storage.all(Place).values()
    city_places = []
    for place in localisation:
        if place.city_id == city_id:
            city_places.append(place.to_dict())
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieve/gets a 'Place' object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a 'Place' object"""
    position = storage.get(Place, place_id)
    if position is None:
        abort(404)
    storage.delete(position)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a new 'Place'"""
    city_ = storage.get(City, city_id)
    if city_ is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user_ = storage.get(User, data['user_id'])
    if user_ is None:
        abort(404)
    data['city_id'] = city_id
    placing = Place(**data)
    placing.save()
    return jsonify(placing.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates 'Place' object"""
    place_ = storage.get(Place, place_id)
    if place_ is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_, k, v)
    place_.save()
    return jsonify(place_.to_dict()), 200
