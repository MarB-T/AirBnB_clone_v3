#!/usr/bin/pyhton3
""" Create routes to get status of the api"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """ return JSON response on api status """
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/status', methods=['GET'])
def get_stats():
    """ return number of objects by type"""
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'states': storage.count('State'),
            'places': storage.count('Place'),
            'users': storage.count('User'),
            'revies': storage.count('Review')
            }
    return jsonify(stats)
