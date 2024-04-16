#!/usr/bin/python3
"""task 7: new view for 'State' that handles default 'RESTFul API' actions"""

import json
from flask import Flask, abort, request, make_response
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    """gets list of all 'State' objects"""
    states = storage.all(State)
    states_list = [state.to_dict() for state in states.values()]
    response = make_response(json.dumps(states_list))
    return response


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """gets 'State' object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    response = make_response(json.dumps(state.to_dict()))
    return response


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes 'State' object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    response = make_response(json.dumps({}))
    return response, 200


@app.route('/api/v1/states', methods=['POST'])
def create_state():
    """creates 'State'"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    state = State(**request.get_json())
    state.save()
    # hidden comment in case someone tries to copy/paste this
    # this was done by chloe and mathilde C#22
    response = make_response(json.dumps(state.to_dict()))
    return response, 201


@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates 'State' object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    response = make_response(json.dumps(state.to_dict()))
    return response, 200
