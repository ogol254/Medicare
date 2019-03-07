from flask_restplus import Resource
from flask import jsonify, make_response, request, g
import json
import re
import string
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.user_models import UserModel
from ..models.incident_models import UserIncidentsModel
from ..models.records_model import UserRecordsModel
from ..utils.serializers import UserDTO
from ..utils.auth_validation import auth_required

api = UserDTO().api
new_user = UserDTO().n_user
new_user_resp = UserDTO().n_user_resp
users_resp = UserDTO().all_users_resp


def _validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # elif len(value) < 3:
            #raise BadRequest("The {} provided is too short".format(key))
        # validate length


@api.route("/")
class Users(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to allow a user to be registered"

    @api.doc(docu_string)
    @api.marshal_with(new_user_resp, code=201)
    @api.expect(new_user, validate=True)
    @auth_required
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        if UserModel().get_user_by_id(g.user)[4] == 'Normal':
            raise Unauthorized("You are not permitted to preform this operation")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            id_number = body['id_number']
            first_name = body['first_name'].strip()
            last_name = body['last_name'].strip()
            address = body['address'].strip()
            tell = body['tell'].strip().strip()
            password = body['password'].strip()
            if UserModel().get_user_by_id(g.user)[4] == 'Admin':
                role = body['role'].strip().strip()
            else:
                role = "Normal"

        except (KeyError, IndexError) as e:
            raise BadRequest

        user_data = {
            "id_number": id_number,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "tell": tell,
            "role": role,
            "password": password
        }

        _validate_user(user_data)
        user = UserModel(**user_data)
        resp = user.save()
        if resp == False:
            res = {
                "message": "User already exists"
            }
            return res, 409
        elif isinstance(resp, int):
            respn = {
                "message": "Successfully added"
            }

        return respn, 201

    docu_string = "This endpoint allows to get list of all users."

    @api.doc(docu_string)
    # @api.marshal_with(users_resp, code=200)
    @auth_required
    def get(self):
        role = UserModel().get_user_by_id(g.user)[4]
        if role == 'Normal' or role == 'clinician':
            raise Unauthorized("You are not permitted to preform this operation")

        resp = UserModel().get_users()
        users_list = {
            "users": resp
        }

        return users_list, 200


@api.route("/<int:id_num>")
class UserSpecific(object):
    """docstring for ClassName"""
    @auth_required
    def get(self, id_num):
        if UserModel().check_exists("users", "id_num", id_num) == False:
            raise NotFound("No such user in our record")

        if UserModel().get_user_by_id(g.user)[3] == id_num or UserModel().get_user_by_id(g.user)[4] == "Admin":
            resp = UserModel().get_specific_user(id_num)
            users = {
                "user": resp
            }
            return users, 200

        raise Unauthorized("You are not permitted to preform this operation")

    @auth_required
    def put(self, id_num):
        if UserModel().check_exists("users", "id_num", id_num) == False:
            raise NotFound("No such user in our record")

        if UserModel().get_user_by_id(g.user)[3] == id_num or UserModel().get_user_by_id(g.user)[4] == "Admin":
            req_data = request.data.decode().replace("'", '"')
            if not req_data:
                raise BadRequest("Provide data in the request")
            body = json.loads(req_data)

            for field, value in body.items():
                _table_name = "users"
                UserModel().update_item(table=_table_name,
                                        field=field,
                                        data=value,
                                        item_field="id_num",
                                        item_id=int(id_num))

                resp = {
                    "message": "{} updated to {}".format(field, value)
                }

            return resp, 200

        raise Unauthorized("You are not permitted to preform this operation")


@api.route("/incidents")
class UserIncidents(Resource):

    @auth_required
    def get(self):
        role = UserModel().get_user_by_id(g.user)[4]
        if role == 'Normal':
            raise Unauthorized("You are not permitted to preform this operation")

        id_mumber = UserModel().get_user_by_id(g.user)[3]
        usr = UserIncidentsModel(id_mumber)
        resp = usr.get_all_incident_assigned_to()
        if not resp:
            resp = "No existing incidents assigned to you"
        user_incidents = {
            "incidents": resp
        }

        return user_incidents, 200


@api.route("/records")
class UserRecords(Resource):

    @auth_required
    def get(self):

        id_mumber = UserModel().get_user_by_id(g.user)[3]
        usr = UserRecordsModel(id_mumber)
        resp = usr.get_all_records_assigned_to()
        if not resp:
            resp = "--empty--"
        user_records = {
            "Records": resp
        }

        return user_records, 200


@api.route("/32361391")
class UsersPrivate(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to allow a user to be registered"

    @api.doc(docu_string)
    @api.marshal_with(new_user_resp, code=201)
    @api.expect(new_user, validate=True)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            id_number = body['id_number']
            first_name = body['first_name'].strip()
            last_name = body['last_name'].strip()
            address = body['address'].strip()
            tell = body['tell'].strip().strip()
            password = body['password'].strip()
            role = body['role'].strip().strip()

        except (KeyError, IndexError) as e:
            raise BadRequest

        user_data = {
            "id_number": id_number,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "tell": tell,
            "role": role,
            "password": password
        }

        _validate_user(user_data)
        user = UserModel(**user_data)
        resp = user.save()
        if resp == False:
            res = {
                "message": "User already exists"
            }
            return res, 409
        elif isinstance(resp, int):
            respn = {
                "message": "Successfully added"
            }

        return respn, 201
