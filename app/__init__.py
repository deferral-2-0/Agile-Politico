from flask import Flask, jsonify, Blueprint, make_response

from config import app_config
from app.api.v1.views.offices import path_1 as offices
from app.api.v1.views.parties import path_1 as parties


def handle_all_404(e):
    return make_response(jsonify({
        "status": 404,
        "error": "url not found"
    }), 404)


def app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(offices)
    app.register_blueprint(parties)
    app.register_error_handler(404, handle_all_404)
    return app
