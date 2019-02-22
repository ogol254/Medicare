from flask_restplus import Resource
from flask import jsonify, make_response, request
import json
import re
import string
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.auth_models import UserModel
from ..utils.serializers import UserDTO
from ..utils.auth_validation import auth_required

api = UserDTO().api
login_user = UserDTO().user
_user_resp = UserDTO().user_resp
_validate_user_resp = UserDTO.validate_user_resp


def _validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # validate length
        if key == "id_number" or key == "password":
            if len(value) < 5:
                raise BadRequest("The {} provided is too short".format(key))
            elif len(value) > 15:
                raise BadRequest("The {} provided is too long".format(key))
        if key == "id_number":
            if value.isdigit() == False:
                raise BadRequest("The {} provided contain either strings or alphanumeric characters".format(key))


@api.route("/signin")
class AuthLogin(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to allow a registered user to log in."

    @api.doc(docu_string)
    #@api.marshal_with(_user_resp, code=200)
    @api.expect(login_user, validate=True)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            return make_response(jsonify({"Message": "Provide data in the request"}))
        login_details = json.loads(req_data)
        id_number = login_details['id_number'].strip()
        password = login_details['password'].strip()

        login_data = {
            "id_number": id_number,
            "password": password
        }

        _validate_user(login_data)

        user = UserModel(**login_data)
        record = user.get_user_by_id(id_number)
        if not record:
            return make_response(jsonify({
                "Message": "Your details were not found, please sign up"
            }), 401)

        first_name, last_name, passwordharsh, id_number, role = record
        if not check_password_hash(passwordharsh, password):
            raise Unauthorized("National Identification number and Password do not match")

        token = user.encode_auth_token(id_number)
        resp = {
            "message": "Success",
            "AuthToken": "{}".format(token.decode('utf-8')),
            "id_number": int(id_number)
        }

        return resp, 200


@api.route('/signout')
class AuthLogout(Resource):
    """This class collects the methods for the  endpoint"""

    def post(self):
        """This endpoint allows a registered user to logout."""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({
                "Message": "No authorization header provided. This resource is secured."
            }), 400)
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # token is either invalid or expired
            return make_response(jsonify({
                "Message": "You are not authorized to access this resource. {}".format(response)
            }), 401)
        else:
            # the token decoded succesfully
            # logout the user
            user_token = UserModel().logout_user(auth_token)
            resp = dict()
            return {"message": "logout successful. {}".format(user_token)}, 200


@api.route('/validate')
class AuthValidate(Resource):
    """This class collects the methods for the questions endpoint"""
    docu_string = "This endpoint validates a token"

    @api.doc(docu_string)
    @api.marshal_with(_validate_user_resp, code=200)
    @auth_required
    def post(self):
        """This endpoint validates a token"""
        user = UserModel().get_user_by_id()
        id_num = int(user[3])
        name = user[0]
        resp = {
            "message": "Valid",
            "id num": "{}".format(id_num),
            "name": name
        }
        return resp, 200
