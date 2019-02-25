from flask_restplus import Resource
from flask import jsonify, make_response, request
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
    def post(self):
        """This endpoint allows an unregistered user to sign up."""

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("authorization header provided. This resource is secured.")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response[0], str):
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource. {}".format(response))
        else:

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
                if response[1] == 'admin':
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
            if False:
                return make_response(jsonify({
                    "message": "User already exists"
                }), 409)
            elif isinstance(resp, int):
                resp = {
                    "message": "Successfully added"
                }

            return resp, 201

    docu_string = "This endpoint allows to get list of all users."

    @api.doc(docu_string)
    @api.marshal_with(users_resp, code=200)
    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("authorization header provided. This resource is secured.")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource. {}".format(response))
        else:
            resp = UserModel().get_users()
            users_list = {
                "message": "Users",
                "users": resp
            }

            return users_list, 200
