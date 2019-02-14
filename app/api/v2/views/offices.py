from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table

from app.api.v2.models.offices import OfficesModel
from app.api.v2.models.users import UserModel
from app.api.v2.models.candidates import CandidateModel

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
    """
        Get all offices from the
        database. No authentication is required here.
    """
    offices = OfficesModel.get_all_offices()
    if offices:
        return utils.response_fn(200, "data", offices)
    return utils.response_fn(200, "data", [])


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
    return utils.response_fn(404, "error", "Office is not not found")


@path_2.route("/offices/<int:office_id>/register", methods=["POST"])
@token_required
def register_candidate_to_office(userobj, office_id):
    """
    this is where we check if the candidates information is
    eligible so that it can be registered to an office.
    """
    try:
        email = userobj[0][0]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    try:
        data = request.get_json()
        user = data["user"]

    except KeyError:
        abort(utils.response_fn(400, "error", "Keys Should be office & user"))

    # check if details are for an admin.
    if email == "tevinthuku@gmail.com":
        # does the candidate & office exist in the db.
        candidate = UserModel.get_user_by_id(user)
        office = OfficesModel.get_specific_office(office_id)
        if candidate and office:
            is_candidate_registered = CandidateModel.check_if_candidate_is_already_registered(
                candidate[0][0], office[0]["id"])
            if is_candidate_registered:
                return utils.response_fn(400, "error", "Candidate is already registerd in this office")
            CandidateModel.register_politician_user_to_office(
                office[0]["id"], candidate[0][0])
            return utils.response_fn(201, "message", "registered candidate")
        else:
            return utils.response_fn(404, "error", "Either candidate or office is missing in db")

    return utils.response_fn(401, "error", "You are not authorized.")
