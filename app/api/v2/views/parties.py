from flask import request, abort

from app.api.v2 import path_2
from app.api import utils

from app.api.v2.models.parties import PartiesModel


@path_2.route("/parties", methods=["GET"])
def get_all_parties():
    """
        This method gets all parties
    """
    parties = PartiesModel.get_all_parties()
    if parties:
        return utils.response_fn(200, "data", parties)
    return utils.response_fn(200, "data", [])
