#!/usr/bin/python3
"""This handles all default RESTFul API actions for place objects"""

from models import storage
from models.place import Place
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.user import User


all_city_ids = []
for key, obj in storage.all(City).items():
    all_city_ids.append(obj.id)

all_user_ids = []
for key, obj in storage.all(User).items():
    all_user_ids.append(obj.id)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_city_place(city_id):
    """This returns a list of all places in a city"""
    all_place = []
    if city_id not in all_city_ids:
        abort(404)
    for key, obj in storage.all(Place).items():
        if obj.city_id == city_id:
            all_place.append(obj.to_dict())

    return jsonify(all_place)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """This returns a place"""
    for key, obj in storage.all(Place).items():
        if obj.id == place_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """This deletes a place object"""
    for key, obj in storage.all(Place).items():
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
            return {}, 200
    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """This creates a new place object"""
    if city_id not in all_city_ids:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    if "name" not in request.json:
        abort(400, "Missing name")
    dict_form = request.get_json()
    dict_form['city_id'] = city_id
    for k, v in dict_form.items():
        if k == 'user_id' and v not in all_user_ids:
            abort(404)
    new_place = Place(**dict_form)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """This updates the attributes of a place"""
    if not request.json:
        abort(400, "Not a JSON")
    dict_form = request.get_json()
    for key, obj in storage.all(Place).items():
        if obj.id == place_id:
            for k, v in dict_form.items():
                if k not in ('id', 'user_id', 'city_id', 'created_at',
                             'updated_at'):
                    setattr(obj, k, v)
                    storage.save()
            return jsonify(obj.to_dict()), 200
    abort(404)
