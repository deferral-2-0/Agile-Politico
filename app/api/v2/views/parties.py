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


@path_2.route("/parties/<int:party_id>", methods=["GET"])
def get_specific_party(party_id):
    """
        This method gets a specific party from the db
    """
    party = PartiesModel.get_specific_party(party_id)
    if party:
        return utils.response_fn(200, "data", party)
    return utils.response_fn(404, "error", "Party not found")


@path_2.route("/parties/<int:party_id>/name", methods=["PATCH"])
@token_required
def update_party(user, party_id):
    """
        This method updates a party if it exists
    """

    try:
        data = request.get_json()
        name = data['name']
    except KeyError:
        abort(utils.response_fn(400, "error", "Provide a name to update"))

    try:
        email = user[0][0]
    except:
        return utils.response_fn(401, "error", "You don't have an account")
    if email == "tevinthuku@gmail.com":
        party = PartiesModel.get_specific_party(party_id)
        if party:
            # update party here
            PartiesModel.update_specific_party(name=name, party_id=party_id)
            return utils.response_fn(200, "data", [{
                "name": name,
                "id": party_id
            }])
        return utils.response_fn(404, "error", "Party not found")
    return utils.response_fn(401, "error", "You are not authorized.")
