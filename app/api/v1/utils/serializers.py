"""
This module collects all the Data Transfer Objects for the API
"""
from flask_restplus import Namespace, fields


class UserDTO(object):
    """User Data Transfer Object"""
    api = Namespace('auth', description='user authentication and signup resources')
    n_user = api.model('new user request', {
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'username': fields.String(required=True, description="user's username"),
        'email': fields.String(required=True, description="user's email address"),
        'password': fields.String(required=True, description="user's password")
    })
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
        'id num': fields.String(required=False, description="userid"),
        'name': fields.String(required=False, description="username")
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
