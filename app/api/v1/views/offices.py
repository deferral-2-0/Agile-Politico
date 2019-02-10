"""All routes pertaining to offices"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1
from app.api.v1.models.offices import OfficesModel, OFFICES

# validate function
from app.api.utils import is_valid_string, response_fn, get_all_items
from app.api.utils import get_specific_item


@path_1.route("/offices", methods=['GET'])
def get_all_offices():
    """
        This function gives access to
        the functionality of viewing all the offices
         in the offices list
    """
    return response_fn(200, "data", get_all_items(OfficesModel, "office"))


@path_1.route("/offices", methods=["POST"])
def create_office():
    """
    This function gives access to the functionality
    of creating a new office
    with the data provided in the post payload of
    this method
    """
    try:
        data = request.get_json()
        type = data['type']
        name = data['name']
    except:
        return response_fn(400, "error", 'Check your json keys. '
                           'Should be type and name')
    if(not is_valid_string(type) or not is_valid_string(name)):
        return response_fn(400, "error", 'The name and type fields'
                           ' are not valid but they are not present')

    office = OfficesModel(
        type=type,
        name=name)
    office.save_office()

    return response_fn(201, "data", [{"id": len(OFFICES) - 1,
                                      "type": type,
                                      "name": name}])


@path_1.route("/offices/<int:office_id>", methods=['GET'])
def get_office(office_id):
    """
    This function gives access to the functionality of
    creating getting an office based on the id provided in the
    url
    """
    office = get_specific_item(OfficesModel, "office", office_id)
    if office:
        return response_fn(200, "data", office)
    return response_fn(404, "error", "We cant find this office")
