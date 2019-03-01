from flask_restplus import Resource
from flask import jsonify, make_response, request, g
import json
import re
import string
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.user_models import UserModel
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
        if UserModel().get_user_by_id(g.user)[4] == 'normal':
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
            if UserModel().get_user_by_id(g.user)[4] == 'admin':
                role = body['role'].strip().strip()
            else:
                role = "normal"

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
            return make_response(jsonify({
                "message": "User already exists"
            }), 409)
        elif isinstance(resp, int):
            respn = {
                "message": "Successfully added"
            }

        return respn, 201

    docu_string = "This endpoint allows to get list of all users."

    @api.doc(docu_string)
    @api.marshal_with(users_resp, code=200)
    @auth_required
    def get(self):
        if UserModel().get_user_by_id(g.user)[4] == 'normal':
            raise Unauthorized("You are not permitted to preform this operation")

        resp = UserModel().get_users()
        users_list = {
            "message": "Users",
            "users": resp
        }

        return users_list, 200


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
