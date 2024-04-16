#!/usr/bin/python3
"""task 9: new view for Amenity handles default RESTFul API actions"""

import json
from flask import abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'])
def get_post_amenities():
    """get + post amenities"""
    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in
                     storage.all(Amenity).values()]
        return json.dumps(amenities)
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            # hidden comment in case someone tries to copy/paste this
            # this was done by chloe and mathilde C#22
            if 'name' not in data:
                abort(400, 'Missing name')
            amenity = Amenity(**data)
            amenity.save()
            return json.dumps(amenity.to_dict()), 201
        except Exception as e:
            abort(400, str(e))


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def del_put_get_amenity(amenity_id):
    """amenity delete + get + put"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return json.dumps(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity.delete()
        return {}, 200
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if not data:
                abort(400, 'Not a JSON')
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            amenity.save()
            return json.dumps(amenity.to_dict()), 200
        except Exception as e:
            abort(400, str(e))
