#!/bin/usr/python3
from flask import abort, request, jsonify
from api.v1.views import app
from models import storage
from models.user import User


@app.route('/api/v1/users', methods=['GET'])
def gets_users():
    """gets/retrieves list of all 'User' objects"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """retrieves a 'User' object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes a 'User' object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """creates a 'User'"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()

    data_insert_fields = ['email', 'password']
    for field in data_insert_fields:
        if field not in data:
            abort(400, description="Missing {}".format(field))
    user = User(**{k: v for k, v in data.items() if k in data_insert_fields})
    user.save()
    return jsonify(user.to_dict()), 201


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates a 'User' object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for attr, value in data.items():
        if attr in ['name', 'password']:
            setattr(user, attr, value)
    user.save()
    return jsonify(user.to_dict()), 200
