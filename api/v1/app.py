#!/usr/bin/python3
"""
script that register the blueprint app_views to your Flask instance app
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_core import CORS
from models import storage
from os import getenv


app = Flask(__name__)


CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})


app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exc):
    """ remove current SQLAlchemy session """
    storage.close()


@app.errorhandler(404)
def not_found():
    """ Handles not found error """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
