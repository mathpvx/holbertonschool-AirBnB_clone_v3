#!/usr/bin/python3
"""new view for Review object that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """ get all reviews of a place"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    json_format = []
    for review in the_place.reviews:
        json_format.append(review.to_dict())
    return jsonify(json_format)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_id(review_id):
    """ get review with a provided id"""
    the_review = storage.get(Review, review_id)
    if the_review is None:
        abort(404)
    else:
        return jsonify(the_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review object if found"""
    the_review = storage.get(Review, review_id)
    if the_review is None:
        abort(404)
    else:
        storage.delete(the_review)
        storage.save()
        return {}, 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ creates a review"""

    """ check and get existing place"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)

    """ check HTTP body request"""
    http_body_request = request.get_json(silent=True)
    if http_body_request is None:
        return "Not a JSON\n", 400
    elif "user_id" not in http_body_request:
        return "Missing user_id\n", 400
    elif "text" not in http_body_request:
        return "Missing text\n", 400
    else:
        """ check user_id"""
        the_user = storage.get(User, http_body_request["user_id"])
        if the_user is None:
            abort(404)
        http_body_request["place_id"] = place_id

        """ create new review"""
        new_review = Review(**http_body_request)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_reveiw(review_id):
    """ updates a given review"""
    the_review = storage.get(Review, review_id)
    ignore_keys_list = ["id", "created_at", "updated_at", "place_id",
                        "user_id"]
    if the_review is None:
        abort(404)
    else:
        http_body_request = request.get_json(silent=True)
        if http_body_request is None:
            return "Not a JSON\n", 400
        else:
            for key, value in http_body_request.items():
                if key not in ignore_keys_list:
                    setattr(the_review, key, value)
        storage.save()
        return jsonify(the_review.to_dict()), 200
