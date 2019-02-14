from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table

from app.api.v2.models.offices import OfficesModel
from app.api.v2.models.users import UserModel
from app.api.v2.models.votes import VotesModel
import psycopg2


@path_2.route("/votes", methods=["POST"])
@token_required
def create_vote(user):
    """
    """
    try:
        user_id = user[0][1]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    try:
        data = request.get_json()
        office = data["office"]
        candidate = data["candidate"]

    except KeyError:
        abort(utils.response_fn(400, "error", "Should be name & address"))

    try:
 
        iscandidatePresent = UserModel.get_user_by_id(candidate)
        isOfficePresent = OfficesModel.get_specific_office(office)
        if iscandidatePresent and isOfficePresent:
            voted = VotesModel.check_if_user_already_voted(user_id, office)
            if voted:
                return utils.response_fn(401, "error", "ALready voted")
            newvote = VotesModel(office, candidate, user_id)
            newvote.save_vote()
            return utils.response_fn(201, "data", "Voted succeffully")
        return utils.response_fn(404, "error", "Either Candidate or party doesn't exist")

    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))
