from flask import Flask, jsonify, Blueprint, make_response

from config import app_config
from app.api.v1.views.offices import path_1 as offices
from app.api.v1.views.parties import path_1 as parties

from app.api.utils import response_fn


def handle_all_404(e):
    """
    Handle all 404 errors in the app. of url not found
    """
    return response_fn(404, "error", "url not found")


def handle_method_not_allowed(e):
    """
        Handle all 405 errors of method not allowed in the app
        This occur when a method is used on a route that does
        not allow the method to be used

    """
    return response_fn(405, "error", "method not allowed")


def app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    app.register_error_handler(404, handle_all_404)
    app.register_error_handler(405, handle_method_not_allowed)
    app.register_blueprint(offices)
    app.register_blueprint(parties)
    return app
