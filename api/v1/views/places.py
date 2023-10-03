#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default RESTFul API
"""
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET']
                 strict_slashes=False)
def get_place_by_city_id(city_id):
    """ get places by city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """get place by id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete place object """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data[user_id])
    if not user:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """handles not found error"""
    response {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """ handles bad request error"""
    response {'error': 'Bad Request'}
    return jsonify(response), 400


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """search places based on given json """
    if request.get_json() is None:
        abort(400, description='Not a JSON')
    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)
    if not data or not len(data) or (not states and not cities
                                     and not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    list_places = []
    if states:
        list_states = [storage.get(State, state_id) for s_id in states]
        for state in list_states:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)
    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)
    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, amenity_id) for amenity_id in
                             amenities]
            list_places = [place for place in list_places
                           if all([am in place.amenities
                                  for am in amenities_obj])]
    places = []
    for plc in list_places:
        d = plc.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
