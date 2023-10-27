#!/usr/bin/python3
"""
create a view for state objects to handle RESTFUL api
"""

from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ retrieves a list of states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ get state by id"""
    state = storage.get(State, state_id)
    if states:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a state objects """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates state """
    if not request.get_json():
        abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update states """
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """handle not found error"""
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """handle bad requests"""
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
