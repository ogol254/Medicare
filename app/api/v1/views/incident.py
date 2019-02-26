import re
import json
import string

# third party packages
from flask_restplus import Resource
from flask import jsonify, make_response, request, g
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

# local imports
from ..models.incident_models import IncidentModel
from ..utils.serializers import IncidentDTO
from ..utils.auth_validation import auth_required

api = IncidentDTO().api
new_inci = IncidentDTO().n_inci
new_inci_resp = IncidentDTO().n_inci_resp
g_resp = IncidentDTO().all_incidents_resp
_g_resp = IncidentDTO().all_inci_resp


def _validate_incident(incident):
    """This function validates the user input and rejects or accepts it"""
    for key, value in incident.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # elif len(value) < 3:
            #raise BadRequest("The {} provided is too short".format(key))
        # validate length


@api.route("/")
class Incidents(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to report an incident"

    @api.doc(docu_string)
    @api.expect(new_inci, validate=True)
    @api.marshal_with(new_inci_resp, code=201)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            name = body['name'].strip()
            location = body['location'].strip()
            type = body['type'].strip()
            tell = body['tell'].strip().strip()
            description = body['description'].strip()

        except (KeyError, IndexError) as e:
            raise BadRequest

        incident_data = {
            "name": name,
            "location": location,
            "type": type,
            "tell": tell,
            "description": description
        }

        _validate_incident(incident_data)
        incident = IncidentModel(**incident_data)
        resp = incident.save()

        response = {
            "message": "Success",
            "incident_id": resp
        }

        return response, 201

    docu_string = "This endpoint allows to get list of all incidents"

    @api.doc(docu_string)
    @api.marshal_with(g_resp, code=200)
    @auth_required
    def get(self):
        resp = IncidentModel().get_all()
        incident_list = {
            "message": "Incidents",
            "incidents": resp
        }

        return incident_list, 200


@api.route('/<int:incident_id>')
class GetSpecifiedIncident(Resource):
    """docstring for GetSpecifiedIncident"""

    docu_string = "This endpoint allows to get a specific incident"

    @api.doc(docu_string)
    @api.marshal_with(g_resp, code=200)
    @auth_required
    def get(self, incident_id):
        if IncidentModel().check_exists("incidents", "incident_id", incident_id) == False:
            raise NotFound("No such incident in our record")

        resp = IncidentModel().get_single_incidents(incident_id)
        incident = {
            "message": "Incident",
            "incidents": resp
        }

        return incident, 200

    @api.marshal_with(g_resp, code=200)
    @auth_required
    def put(self, incident_id):
        if IncidentModel().check_exists("incidents", "incident_id", incident_id) == False:
            raise NotFound("No such incident in our record")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)

        for field, value in body.items():
            _table_name = "incidents"
            IncidentModel().update_item(table=_table_name,
                                        field=field,
                                        data=value,
                                        item_field="incident_id",
                                        item_id=int(incident_id))

            resp = {
                "message": "{} updated to {}".format(field, value),
                "incidents": incident_id
            }

        return resp, 200
