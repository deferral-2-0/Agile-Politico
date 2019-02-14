from app.api.utils import response_fn

from app.api.v1.views.parties import path_1 as parties
from app.api.v1.views.offices import path_1 as offices


from app.api.v2.views.users import path_2 as users
from app.api.v2.views.parties import path_2 as v2parties
from app.api.v2.views.offices import path_2 as v2offices
from app.api.v2.models.db import init_db

"""

This is where we initialize the app
by creating a factory function, where all the blueprints and
the errors are handled

"""

from flask import Flask, jsonify, make_response
from config import app_config

"""

Will still support v1 to minimize breaking changes for my API consumers.
Will be removing V1 in the next 6 months.

"""


"""

v2 configuration objects and functions.

"""


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
    flaskapp.app_context().push()
    flaskapp.url_map.strict_slashes = False
    flaskapp.register_error_handler(404, handle_all_404)
    flaskapp.register_error_handler(405, handle_method_not_allowed)
    """
    v1 blueprints
    """
    flaskapp.register_blueprint(offices)
    flaskapp.register_blueprint(parties)
    """
    v2 blueprints & configuration
    """
    flaskapp.register_blueprint(users)
    flaskapp.register_blueprint(v2parties)
    flaskapp.register_blueprint(v2offices)
    if config_name != "testing":
        """
        dont initialize the db twice while testing.
        It has already been initialized before the
        tests run.
        """
        init_db()
    return flaskapp
