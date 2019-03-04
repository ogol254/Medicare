import re
import json
import string

# third party packages
from flask_restplus import Resource
from flask import jsonify, make_response, request, g
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

# local imports
from ..models.records_model import RecordModel
from ..models.comment_models import CommentModel
from ..utils.serializers import RecordDTO
from ..utils.auth_validation import auth_required

api = RecordDTO().api
new_record = RecordDTO().n_record
new_record_resp = RecordDTO().n_record_resp
all_record = RecordDTO().all_records_resp
single_record_resp = RecordDTO().single_record_resp
g_resp = RecordDTO().get_single_record
gc_resp = RecordDTO().comments


def _validate_record(record):
    """This function validates the user input and rejects or accepts it"""
    for key, value in record.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))


@api.route("/")
class Records(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to report an record"

    @api.doc(docu_string)
    @api.expect(new_record, validate=True)
    @api.marshal_with(new_record_resp, code=201)
    @auth_required
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            incident_id = body['incident_id']
            location = body['location'].strip()
            type = body['type'].strip()
            id_num = body['id_num']
            description = body['description'].strip()
            facility_id = body['facility_id']

            if RecordModel().check_exists("incidents", "incident_id", incident_id) == False:
                raise BadRequest("This incident does not exist")

            if not RecordModel().get_user_by_id(id_num):
                raise BadRequest("This user does not exist in our users list, please create account first")

            if RecordModel().check_exists("facilities", "facility_id", facility_id) == False:
                raise BadRequest("This facility does not exist")

        except (KeyError, IndexError) as e:
            raise BadRequest

        record_data = {
            "incident_id": incident_id,
            "created_by": g.user,
            "id_num": id_num,
            "type": type,
            "description": description,
            "location": location,
            "facility_id": facility_id
        }

        _validate_record(record_data)
        record = RecordModel(**record_data)
        resp = record.save()

        response = {
            "message": "Success",
            "record_id": resp
        }

        return response, 201

    docu_string = "This endpoint allows to get list of all records"

    @api.doc(docu_string)
    @api.marshal_with(all_record, code=200)
    @auth_required
    def get(self):
        if RecordModel().get_user_by_id(g.user)[4] == 'Normal':
            raise Unauthorized("You are not permitted to preform this operation")

        resp = RecordModel().get_all()
        record_list = {
            "message": "records",
            "records": resp
        }

        return record_list, 200


@api.route('/<int:record_id>')
class GetSpecifiedRecord(Resource):
    """docstring for GetSpecifiedrecord"""

    docu_string = "This endpoint allows to get a specific record"

    @api.doc(docu_string)
    @api.marshal_with(g_resp, code=200)
    @auth_required
    def get(self, record_id):
        if RecordModel().check_exists("records", "record_id", record_id) == False:
            raise NotFound("No such record in our record")

        record = RecordModel().get_single_records(record_id)
        comments = CommentModel().get_specif_record_comments(record_id)
        if not comments:
            comments = "No comments exists"
        record = {
            "message": "record",
            "records": record,
            "comments": comments
        }

        return record, 200

    @api.marshal_with(all_record, code=200)
    @auth_required
    def put(self, record_id):
        if RecordModel().check_exists("records", "record_id", record_id) == False:
            raise NotFound("No such record in our record")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)

        for field, value in body.items():
            _table_name = "records"
            RecordModel().update_item(table=_table_name,
                                      field=field,
                                      data=value,
                                      item_field="record_id",
                                      item_id=int(record_id))

            resp = {
                "message": "{} updated to {}".format(field, value),
                "records": record_id
            }

        return resp, 200
