#!/usr/bin/python3
"""
Create a view for a review objects """

from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """ get review by place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [reviews.to_dict() for review in place.review]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ get review by id """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_review.route('/reviews/<review_id>', methods=['DELETE'],
                  strict_slashes=False)
def delete_review(review_id):
    """ delete review """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/place/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create review by place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<reviews_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ update a review by id """
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """ handle not found error"""
    resp = {'error': 'Not found'}
    return jsonify(resp), 404


@app_views.errorhandler(400)
def bad_request(error):
    """ handle bad request error"""
    resp = {'errror': 'Bad Request'}
    return jsonify(resp), 400
