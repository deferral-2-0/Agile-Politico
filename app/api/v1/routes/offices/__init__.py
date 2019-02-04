"""All routes pertaining to offices"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1


@path_1.route("/offices", methods=['GET'])
def get_all_offices():
    """
    fetch_all_offices (initial test)
    """
    return make_response(jsonify({"status": 200, "data": []}), 200)
