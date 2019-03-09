from flask_restplus import Resource
from flask import jsonify, make_response, request, g
import json
import re
import string
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.auth_models import AuthModel
from ..utils.serializers import AuthDTO
from ..utils.auth_validation import auth_required

api = AuthDTO().api
login_user = AuthDTO().user
_user_resp = AuthDTO().user_resp
_validate_user_resp = AuthDTO().validate_user_resp


def _validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # validate length
        if key == "password":
            if len(value) < 5:
                raise BadRequest("The {} provided is too short".format(key))
            elif len(value) > 15:
                raise BadRequest("The {} provided is too long".format(key))


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
            raise BadRequest("Provide data in the request")
        login_details = json.loads(req_data)
        id_number = login_details['id_number']
        password = login_details['password'].strip()

        login_data = {
            "id_number": id_number,
            "password": password
        }

        _validate_user(login_data)

        user = AuthModel(**login_data)
        record = AuthModel().get_user_by_id(id_number)
        if not record:
            return make_response(jsonify({
                "message": "Your details were not found, please sign up"
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
            raise BadRequest("authorization header provided. This resource is secured.")
        auth_token = auth_header.split(" ")[1]
        response = AuthModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource. {}".format(response))
        else:
            # the token decoded succesfully
            # logout the user
            user_token = AuthModel().logout_user(auth_token)
            resp = dict()
            return {"message": "logout successful. {}".format(user_token)}, 200


@api.route('/validate')
class AuthValidate(Resource):
    """This class collects the methods for the questions endpoint"""
    docu_string = "This endpoint validates a token"

    @api.doc(docu_string)
#     @api.marshal_with(_validate_user_resp, code=200)
    @auth_required
    def post(self):
        """This endpoint validates a token"""
        user = AuthModel().get_user_by_id(g.user)
        id_num = int(user[3])
        name = user[0]
        resp = {
            "message": "Valid",
            "id_num": id_num,
            "name": name
        }
        return resp, 200
