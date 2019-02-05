"""All routes pertaining to parties"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1
from app.api.v1.model import PartiesModel, PARTIES


@path_1.route("/parties", methods=['GET'])
def get_all_parties():
    """
    fetch_all_parties
    """
    parties = PartiesModel.get_all_parties()
    return make_response(jsonify({"status": 200, "data": parties}), 200)


@path_1.route("/parties", methods=["POST"])
def create_party():
    try:
        data = request.get_json()
        id = data['id']
        name = data['name']
    except:
        return jsonify({'status': 400,
                        'error': "Check your json keys. Should be name and id"})
    party = PartiesModel(id=id,
                         name=name)
    party.save_party()
    return make_response(jsonify({"status": 201,
                                  "data": [{"id": id,
                                            "name": name}]}), 201)
