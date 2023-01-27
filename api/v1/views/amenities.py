#!/usr/bin/python3
"""This creates the view for amenity object"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def all_amenities():
    """This returns the list of all amenity objects"""
    all_amenities = []
    for key, obj in storage.all(Amenity).items():
        all_amenities.append(obj.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """This returns a specific amenity"""
    for key, obj in storage.all(Amenity).items():
        if obj.id == amenity_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """This remove an amenity from storage"""
    for key, obj in storage.all(Amenity).items():
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
            return {}, 200
    abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """This creates a new amenity object"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    dict_form = request.get_json()
    new_amenity = Amenity(**dict_form)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """This updates the attributes of an amenity object"""
    if not request.json:
        abort(400, "Not a JSON")
    dict_form = request.get_json
    for key, obj in storage.all(Amenity).items():
        if obj.id == amenity_id:
            for k, v in dict_form.items():
                if k not in ('id', 'created_at', 'updated_at'):
                    setattr(obj, k, v)
                    storage.save()
            return jsonify(obj.to_dict()), 200
    abort(404)
