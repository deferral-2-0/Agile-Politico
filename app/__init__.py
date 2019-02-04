from flask import Flask, jsonify, Blueprint

from config import app_config
from app.api.v1.routes.offices import path_1 as offices


def app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(offices)

    return app
