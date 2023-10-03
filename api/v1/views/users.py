#!/usr/bin/python3
"""
Creates a new view for User object that handles RESTFul api
"""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ gets all users """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/user/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ gets user by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ delete user """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', method=['POST'],
                 strict_slashes=False)
def create_user():
    """ creates a user object """
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/user/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update user """
    user = storage.get(User, user_id)
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200
        else:
            abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """ handle not found errors """
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """ handles bad request"""
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
