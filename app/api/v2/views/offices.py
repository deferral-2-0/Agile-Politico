from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table

from app.api.v2.models.offices import OfficesModel
from app.api.v2.models.users import UserModel
from app.api.v2.models.candidates import CandidateModel

from ..utils import isUserAdmin

import psycopg2


@path_2.route("/offices", methods=["POST"])
@token_required
def create_office(user):
    """
        This method allows the admin to creates a specific office to the database
    """
    try:
        userAdminProperty = user[0][2]
    except:
        return utils.response_fn(401, "error",
                                 "You don't have an account, Create one first")

    try:
        data = request.get_json()
        name = data['name']
        type = data["type"]

    except KeyError:
        abort(utils.response_fn(400, "error",
                                "Should be name & type, enter both fields"))

    try:

        """
            if email matches, admin's then create the party
        """
        # check if details are for an admin.
        isUserAdmin(userAdminProperty)
        # check if inputs are all strings
        utils.check_for_strings(data, ["name", "type"])
        # check if fields are blank
        utils.check_for_whitespace(data, ["name", "type"])
        check_matching_items_in_db_table({"name": name}, "offices")
        newoffice = OfficesModel(
            name=name, type=type)

        id = newoffice.save_office()
        return utils.response_fn(201, "data", [{
            "name": name,
            "id": id,
            "type": type
        }])

    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))


@path_2.route("/offices", methods=['GET'])
def get_all_offices():
    """
        Get all offices from the
        database. No authentication is required here.
    """
    return utils.response_fn(200, "data", OfficesModel.get_all_offices())


@path_2.route("/offices/<int:office_id>", methods=["GET"])
def get_specific_office(office_id):
    """
        This method gets a specific office from
        the list of offices created by the ADMIN.
        No auth is required here.
    """
    office = OfficesModel.get_specific_office(office_id)
    if office:
        return utils.response_fn(200, "data", office)
    return utils.response_fn(404, "error", "Office is not found")


@path_2.route("/offices/<int:office_id>/register", methods=["POST"])
@token_required
def register_candidate_to_office(userobj, office_id):
    """
    this is where we check if the candidates information is
    eligible so that it can be registered to an office.
    """
    try:
        userAdminProperty = userobj[0][2]
    except:
        abort(utils.response_fn(401, "error",
                                "You don't have an account Create one"))

    try:
        data = request.get_json()
        user = data["user"]

    except KeyError:
        abort(utils.response_fn(400, "error", "User key should be present"))

    # check if details are for an admin.
    isUserAdmin(userAdminProperty)
    # check if fields are integers.
    utils.check_for_ints(data, ["user"])
    # does the candidate & office exist in the db.
    candidate = UserModel.get_user_by_id(user)
    office = OfficesModel.get_specific_office(office_id)
    if candidate and office:
        is_candidate_registered = CandidateModel.check_if_candidate_is_already_registered(
            user, office_id)
        if is_candidate_registered:
            abort(utils.response_fn(400, "error",
                                    "Candidate is already registered in this office"))

        # register the politician user.to a certain office.
        CandidateModel.register_politician_user_to_office(
            office_id, user)
        return utils.response_fn(201, "data", [{
            "office": office_id,
            "user": user
        }])
    else:
        return utils.response_fn(404, "error",
                                 "Either candidate or office is missing in the database")


@path_2.route("/offices/<int:office_id>/result", methods=["GET"])
def get_office_results(office_id):
    return utils.response_fn(200, "data", OfficesModel.get_office_results(office_id))


@path_2.route("/offices/<int:office_id>/candidates", methods=["GET"])
def get_candidates(office_id):
    return utils.response_fn(200, "data", OfficesModel.get_all_candidates(office_id))


@path_2.route("/offices/metainfo", methods=["GET"])
def get_meta_info():
    return utils.response_fn(200, "data", OfficesModel.get_meta_info())
