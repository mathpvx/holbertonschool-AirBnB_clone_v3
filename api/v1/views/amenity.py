#!/usr/bin/python3
"""task 9: create new view 'Amenity' handles default 'RESTFul API' actions"""

from flask import abort, request, jsonify
from models import storage
from models.state import State
from models.city import City


@app.route('/api/v1/amenities', methods=['GET'])
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    """Creates a new Amenity"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
