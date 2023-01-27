#!/usr/bin/python3

"""
Flask App that integrates with AirBnB static HTML Template
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import os


app = Flask(__name__)

app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close(exception):
    """
    this method calls .close()
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """json 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    """
    MAIN Flask App
    """
    app.run(host=host, port=port, threaded=True)
