from flask_restplus import Resource
from flask import jsonify, make_response, request, g
import json
import re
import string
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.userbio_models import UserBioModel
from ..utils.serializers import UserBioDTO
from ..utils.auth_validation import auth_required

api = UserBioDTO().api
new_user = UserBioDTO().n_user
new_user_resp = UserBioDTO().n_user_resp
users_resp = UserBioDTO().all_users_resp


@api.route("/")
class UserBio(Resource):
    """This class collects the methods for the auth/signin method"""

    docu_string = "This endpoint accepts POST requests to allow a user to be registered"

    @api.doc(docu_string)
    @api.marshal_with(new_user_resp, code=201)
    @api.expect(new_user, validate=True)
    @auth_required
    def post(self, id_number):
        """This endpoint allows an unregistered user to sign up."""
        if UserBioModel().get_user_by_id(g.user)[4] == 'normal':
            raise Unauthorized("You are not permitted to preform this operation")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)
        try:
            dob = body['date_of_birth'].strip()

        except (KeyError, IndexError) as e:
            raise BadRequest

        user_data = {
            "id_number": id_number,
            "date_of_birth": dob
        }

        user = UserBioModel(**user_data)
        resp = user.save()
        if resp == False:
            res = {
                "message": "Userbio already exists"
            }
            return res, 409
        elif resp == None:
            res = {
                "message": "No such user"
            }
            return res, 404
        elif isinstance(resp, int):
            respn = {
                "message": "Successfully added"
            }

        return respn, 201

    docu_string = "This endpoint allows to get list of all users."

    @api.doc(docu_string)
    #@api.marshal_with(users_resp, code=200)
    @auth_required
    def get(self, id_number):
        resp = UserBioModel().get_user_bio(id_number)
        if resp == False:
            res = {
                "message": "No bio exists"
            }
            return res, 404
        users_list = {
            "data": [resp]
        }

        return users_list, 200

    def put(self, id_number):
        if UserBioModel().check_exists("bio", "id_number", id_number) == False:
            raise NotFound("No such bio in our record, please create one first")

        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        body = json.loads(req_data)

        for field, value in body.items():
            _table_name = "bio"
            UserBioModel().update_item(table=_table_name,
                                       field=field,
                                       data=value,
                                       item_field="id_number",
                                       item_id=int(id_number))

            resp = {
                "message": "{} updated to {}".format(field, value),
                "name": UserBioModel().get_name(id_number)
            }

        return resp, 200
