#!/usr/bin/python3
"""
script to handle all defaults Restful api
"""

from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, request, make_response
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@app_from('documentation/place_amenity/get_places_amenities.yml',
          methods=['GET'])
def get_place_amenities(place_id):
    """ get amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """deletes amenities of a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """link an amenity object to place objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
