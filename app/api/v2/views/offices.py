from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table

from app.api.v2.models.offices import OfficesModel

import psycopg2


@path_2.route("/offices", methods=["POST"])
@token_required
def create_office(user):
    """
        This method allows the admin to creates a specific office to the database
    """
    try:
        email = user[0][0]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    try:
        data = request.get_json()
        name = data['name']
        type = data["type"]

    except KeyError:
        abort(utils.response_fn(400, "error", "Should be name & address"))

    try:

        """
            if email matches, admin's then create the party
        """
        if email == "tevinthuku@gmail.com":
            newoffice = OfficesModel(
                name=name, type=type)

            check_matching_items_in_db_table({"name": name}, "offices")

            newoffice.save_office()

            return utils.response_fn(201, "data", [{
                "name": name
            }])

        return utils.response_fn(401, "error", "You are not an admin")

    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))


@path_2.route("/offices", methods=['GET'])
def get_all_offices():
    offices = OfficesModel.get_all_offices()
    if offices:
        return utils.response_fn(200, "data", offices)
    return utils.response_fn(200, "data", [])
