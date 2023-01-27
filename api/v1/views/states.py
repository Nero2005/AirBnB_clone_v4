#!/usr/bin/python3
"""
Flask route that returns json status response
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """This retrieves the list of all State objects"""
    state_list = []
    for key, obj in storage.all(State).items():
        state_list.append(obj.to_dict())
    return state_list


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """This returns a state that matches state_id"""
    for key, obj in storage.all(State).items():
        if obj.id == state_id:
            return obj.to_dict()
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """This removes the state object of id from storage"""
    for key, obj in storage.all(State).items():
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
            return {}, 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """This creates a new state object"""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    dict_form = request.get_json()
    new_state = State(**dict_form)
    storage.new(new_state)
    storage.save()

    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """This updates the attributes of a State object of id"""
    if not request.json:
        abort(400, "Not a JSON")
    dict_form = request.get_json()
    for key, obj in storage.all(State).items():
        if obj.id == state_id:
            for k, v in dict_form.items():
                if key in ('id', 'created_at', 'updated_at'):
                    pass
                else:
                    obj.k = v
                    storage.save()
            return obj.to_dict(), 200
    abort(404)
