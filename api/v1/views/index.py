#!/usr/bin/python3
"""
Flask route that returns json status response
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats')
def stats():
    """This returns the number of each object type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    all_classes = [Amenity, City, Place, Review, State, User]
    all_keys = ["amenities", "cities", "places", "reviews", "states",
                "users"]
    result = {}
    n = 0

    for obj in all_classes:
        ret = storage.count(obj)
        result[all_keys[n]] = ret
        n += 1

    return result
