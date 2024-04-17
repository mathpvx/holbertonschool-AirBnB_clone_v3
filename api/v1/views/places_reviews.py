#!/usr/bin/python3
"""Reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """Retrieves the list of review+creates"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')
        review = Review(**data)
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    """retrieves a reviews+deletes+updates"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        review.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
