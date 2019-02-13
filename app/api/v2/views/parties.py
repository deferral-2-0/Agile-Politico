from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table

from app.api.v2.models.parties import PartiesModel

import psycopg2


@path_2.route("/parties", methods=["GET"])
def get_all_parties():
    """
        This method gets all parties
    """
    parties = PartiesModel.get_all_parties()
    print(parties)
    if parties:
        return utils.response_fn(200, "data", parties)
    return utils.response_fn(200, "data", [])


@path_2.route("/parties", methods=["POST"])
@token_required
def create_party(user):
    """
        This method allows the admin to creates a specific party to the database
    """
    try:
        email = user[0][0]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    try:
        data = request.get_json()
        name = data['name']
        hqAddress = data["hqAddress"]
        logoUrl = data.get("logoUrl", "")

    except KeyError:
        abort(utils.response_fn(400, "error", "Should be name, hqAddress & logoUrl"))

    try:

        """
            if email matches, admin's then create the party
        """
        if email == "tevinthuku@gmail.com":
            newparty = PartiesModel(
                name=name, hqAddress=hqAddress, logoUrl=logoUrl)

            check_matching_items_in_db_table({"name": name}, "parties")

            newparty.save_party()

            return utils.response_fn(201, "data", [{
                "name": name
            }])

        return utils.response_fn(401, "error", "You are not an admin")

    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))

    # try:
    #     """
    #     check if email is admins' email
    #     """
    #     if email == "tevinthuku@gmail.com":
    #         # create party
    #         newparty = PartiesModel()

    #     return utils.response_fn(401, "error", "You are not authorized to create a party")
