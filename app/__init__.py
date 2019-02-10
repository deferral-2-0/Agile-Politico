"""

This is where we initialize the app
by creating a factory function, where all the blueprints and
the errors are handled

"""

from flask import Flask, jsonify, make_response

from config import app_config
from app.api.v1.views.offices import path_1 as offices
from app.api.v1.views.parties import path_1 as parties

from app.api.utils import response_fn


def handle_all_404(*_):
    """
    Handle all 404 errors in the app. of url not found
    """
    return response_fn(404, "error", "url not found")


def handle_method_not_allowed(*_):
    """
        Handle all 405 errors of method not allowed in the app
        This occur when a method is used on a route that does
        not allow the method to be used

    """
    return response_fn(405, "error", "method not allowed")


def app(config_name):
    """
        Factory function where
        an instance of a flask
        app is created & blueprints are
        registered.
    """
    flaskapp = Flask(__name__)
    flaskapp.config.from_object(app_config[config_name])
    flaskapp.url_map.strict_slashes = False
    flaskapp.register_error_handler(404, handle_all_404)
    flaskapp.register_error_handler(405, handle_method_not_allowed)
    flaskapp.register_blueprint(offices)
    flaskapp.register_blueprint(parties)
    return flaskapp
