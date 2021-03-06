from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table
from app.api.v2.utils import isUserAdmin
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
        This method allows the admin to creates a
        specific party to the database
    """
    try:
        userAdminProp = user[0][2]
    except:
        return utils.response_fn(401, "error",
                                 "You don't have an account. Create One")

    try:
        data = request.get_json()
        name = data['name']
        hqAddress = data["hqAddress"]
        logoUrl = data.get("logoUrl", "")

    except KeyError:
        abort(utils.response_fn(400, "error", "Should be name, hqAddress & logoUrl"))
    # check for the datatype
    utils.check_for_strings(data, ["name", "hqAddress", "logoUrl"])
    # check for whitespaces.
    utils.check_for_whitespace(data, ["name", "hqAddress"])
    try:

        """
            if email matches, admin's then create the party
        """
        # check if the user is an admin
        isUserAdmin(userAdminProp)
        newparty = PartiesModel(
            name=name, hqAddress=hqAddress, logoUrl=logoUrl)
        check_matching_items_in_db_table({"name": name}, "parties")
        id = newparty.save_party()
        return utils.response_fn(201, "data", [{
            "name": name,
            "id": id
        }])
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
    return utils.response_fn(404, "error", "Party is not found")


@path_2.route("/parties/<int:party_id>/name", methods=["PATCH"])
@token_required
def update_party(user, party_id):
    """
        This method updates a party if it exists
    """

    try:
        """
            is the name attr in the payload of the request?
            if not throw an error
        """
        data = request.get_json()
        name = data['name']
    except KeyError:
        abort(utils.response_fn(400, "error", "Provide a name to update"))

    try:
        """
            is the isAdmin prop is present or empty
            if its empty then the user does not have an account.
        """
        userAdminProp = user[0][2]
    except:
        return utils.response_fn(401, "error", "You don't have an account")
    # check if the user is an admin
    isUserAdmin(userAdminProp)
    # check if data we want to apply strip on is actually a string.
    utils.check_for_strings(data, ["name"])
    # check if data is present ans is not just an empty string..
    utils.check_for_whitespace(data, ["name"])
    party = PartiesModel.get_specific_party(party_id)
    if party:
        # update party here
        PartiesModel.update_specific_party(name=name, party_id=party_id)
        return utils.response_fn(200, "data", [{
            "name": name,
            "id": party_id
        }])
    return utils.response_fn(404, "error", "Party is not found")


@path_2.route("/parties/<int:party_id>", methods=["DELETE"])
@token_required
def delete_party(user, party_id):
    try:
        """
            does the request agent have an account @
            politico.
        """
        userAdminProp = user[0][2]
    except:
        return utils.response_fn(401, "error", "You don't have an account")
    # check if the user is an admin user.
    isUserAdmin(userAdminProp)
    party = PartiesModel.get_specific_party(party_id)
    if party:
        # delete party here
        PartiesModel.delete_specific_party(party_id)
        return utils.response_fn(200, "data", [{
            "message": "The party with id {} has been deleted".format(party_id)
        }])
    return utils.response_fn(404, "error", "The party does not exist")
