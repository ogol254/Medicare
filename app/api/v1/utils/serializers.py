"""
This module collects all the Data Transfer Objects for the API
"""
from flask_restplus import Namespace, fields


class AuthDTO(object):
    """User Data Transfer Object"""
    api = Namespace('auth', description='user authentication and signup resources')
    user = api.model('login request', {
        'id_number': fields.String(required=True, description="user's id number"),
        'password': fields.String(required=True, description="user's password")
    })
    user_resp = api.model('response to login', {
        'message': fields.String(required=True, description="success or fail message"),
        'AuthToken': fields.String(required=True, description="authentication token"),
        'id_number': fields.Integer(required=True, description="user's id number")
    })
    validate_user_resp = api.model('validation request', {
        'message': fields.String(required=True, description="success message"),
        'id num': fields.String(required=False, description="user id"),
        'name': fields.String(required=False, description="name")
    })


class UserDTO(object):
    """docstring for  UserDTO"""
    api = Namespace('auth', description='user and signup resources')
    n_user = api.model('new user request', {
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'id_number': fields.Integer(required=True, description="user's id_number"),
        'address': fields.String(required=True, description="user's address address"),
        'password': fields.String(required=True, description="user's password"),
        'tell': fields.String(required=True, description="user's tell"),
        'role': fields.String(required=False, description="user's role")
    })
    n_user_resp = api.model('Reesponse for adding a new user', {
        'message': fields.String(required=True, description="success message")
    })
    all_users_resp = api.model('Reesponse for adding a new user', {
        'message': fields.String(required=True, description="success message"),
        'users' : fields.String(required=True, description="User message")
    })
    all_user_list_resp = api.model('Reesponse for adding a new user', {
        'id_numbers': fields.Integer(required=True, description="user's id_number"),
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'tell': fields.String(required=True, description="user's tell"),
        'address': fields.String(required=True, description="user's address address")
    })



class IncidentDTO(object):
    """incident Data Transfer Object"""
    api = Namespace('incident', description='Incidents Proceses')
    n_incident = api.model('new incident post  request', {
        'description': fields.String(required=True, description="description of the incident"),
        'location': fields.String(required=True, description="location"),
        'incident_type': fields.String(required=True, description="type of the incident"),
    })


class CommentDTO(object):
    """docstring for comments posting"""
    api = Namespace('comment', description='comments Proceses')
    n_comment = api.model('new comment post  request', {
        'comment': fields.String(required=True, description="description of the comment"),
        'incident_id': fields.Integer(required=True, description="incident_id")
    })
