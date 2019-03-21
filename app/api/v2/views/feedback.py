from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.utils import token_required, check_matching_items_in_db_table
from app.api.v2.models.feedback import FeedbackModel

import psycopg2


@path_2.route("/feedback", methods=["GET"])
def get_all_feedback():
    """
        This method gets all the posted feedback
    """
    feedback = FeedbackModel.get_all_feedback()
    if feedback:
        return utils.response_fn(200, "data", feedback)
    return utils.response_fn(200, "data", [])


@path_2.route("/feedback", methods=["POST"])
@token_required
def create_feedback(user):
    """
        Post feedback
    """
    try:
        user_id = user[0][1]
    except:
        return utils.response_fn(401, "error", "You don't have an account")

    try:
        data = request.get_json()
        body = data["body"]
        utils.check_for_whitespace(data, ["body"])
        utils.is_valid_string(body)

    except KeyError:
        abort(utils.response_fn(400, "error",
                                "Feedback body is required"))
    try:
        """
            record feedback
        """
        feedback = FeedbackModel(
            voter=user_id, body=body)
        check_matching_items_in_db_table({"body": body}, "feedback")
        feedback.save_feedback()
        return utils.response_fn(201, "data", [{
            "body": body,
            "message": "feedback submitted successfully"
        }])
    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))