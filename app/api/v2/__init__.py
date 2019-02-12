# Declare the api prefix for v2 of the app

from flask import Blueprint
path_2 = Blueprint("apiv2", __name__, url_prefix="/api/v2")
