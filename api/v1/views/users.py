#!/usr/bin/python3
"""
This is module users
"""
from api.v1.views import app_views
from flask import (abort, jsonify, make_response, request)
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def view_user(user_id=None):
    """Example endpoint returning a list of all users or of one specified
    Retrieves a list of all users or of one specified by user_id
    """
    if user_id is None:
        all_users = [state.to_json() for state
                     in storage.all(User).values()]
        return jsonify(all_users)
    s = storage.get(User, user_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id=None):
    """Example endpoint deleting one user
    Deletes a user based on the user_id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Example endpoint creates a user
    Creates a user based on the JSON body
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'email' not in r.keys():
        return "Missing email", 400
    if 'password' not in r.keys():
        return "Missing password", 400
    s = User(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """Example endpoint updates a user
    Updates a user based on the JSON body
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    a = storage.get(User, user_id)
    if a is None:
        abort(404)
    for k in ("id", "email", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200
