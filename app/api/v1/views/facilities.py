import re
import json
import string

# third party packages
from flask_restplus import Resource
from flask import jsonify, make_response, request, g
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

# local imports
from ..models.facilities_models import FacilityModel
from ..utils.serializers import FacilitiesDTO
from ..utils.auth_validation import auth_required

api = FacilitiesDTO().api
new_facility = FacilitiesDTO().n_facility
new_facility_resp = FacilitiesDTO().n_facility_resp
all_resp = FacilitiesDTO()._facility_resp


def _validate_(facility):
    """This function validates the user input and rejects or accepts it"""
    for key, value in facility.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # elif len(value) < 3:
            #raise BadRequest("The {} provided is too short".format(key))
        # validate length


@api.route('/')
class Facility(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to report an facility"

    @api.doc(docu_string)
    @api.expect(new_facility, validate=True)
    @api.marshal_with(new_facility_resp, code=201)
    @auth_required
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        if FacilityModel().get_user_by_id(g.user)[4] != 'admin':
            raise Unauthorized("You are not permitted to preform this operation")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            name = body['name'].strip()
            location = body['location'].strip()
            contact = body['contact'].strip()

        except (KeyError, IndexError) as e:
            raise BadRequest

        facility_data = {
            "name": name,
            "created_by": g.user,
            "location": location,
            "contact": contact
        }

        _validate_(facility_data)
        facility = FacilityModel(**facility_data)
        resp = facility.save_facility()

        response = {
            "message": "Success",
            "facility_id": resp
        }

        return response, 201

    docu_string = "This endpoint allows to get list of all facilities"

    @api.doc(docu_string)
    @api.marshal_with(all_resp, code=200)
    @auth_required
    def get(self):
        if FacilityModel().get_user_by_id(g.user)[4] != 'admin':
            raise Unauthorized("You are not permitted to preform this operation")

        resp = FacilityModel().get_all()
        facilities_list = {
            "message": "Success",
            "facilities": resp
        }
        return facilities_list, 200


@api.route('/<int:facility_id>')
class GetSpecificFacility(Resource):
    """docstring for GetSpecifiedfacility"""

    @api.marshal_with(new_facility_resp, code=200)
    @auth_required
    def put(self, facility_id):
        if FacilityModel().check_exists("facilities", "facility_id", facility_id) == False:
            raise NotFound("No such facility in our database")

        if FacilityModel().get_user_by_id(g.user)[4] != 'admin':
            raise Unauthorized("You are not permitted to preform this operation")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)

        for field, value in body.items():
            _table_name = "facilities"
            FacilityModel().update_item(table=_table_name,
                                        field=field,
                                        data=value,
                                        item_field="facility_id",
                                        item_id=int(facility_id))

            resp = {
                "message": "{} updated to {}".format(field, value),
                "facility_id": facility_id
            }

        return resp, 200

    @api.marshal_with(all_resp, code=200)
    @auth_required
    def get(self, facility_id):
        if FacilityModel().check_exists("facilities", "facility_id", facility_id) == False:
            raise NotFound("No such facility in our database")

        if FacilityModel().get_user_by_id(g.user)[4] != 'admin':
            raise Unauthorized("You are not permitted to preform this operation")

        resp = FacilityModel().get_single_facility(facility_id)
        facility = {
            "message": "Success",
            "facilities": resp
        }
        return facility, 200
