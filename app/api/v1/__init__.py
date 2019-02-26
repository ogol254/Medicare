"""
This module sets up the users resource
Authored by: Ogol
"""
from flask_restplus import Api
from flask import Blueprint
from werkzeug.exceptions import NotFound

version_one = Blueprint('version1', __name__, url_prefix="/api/v1")

from .views.auth import api as auth_ns
from .views.users import api as user_ns
from .views.incident import api as inci_ns


api = Api(version_one,
          title='Medicare API',
          version='1.0',
          description="Meternal health support system")

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(user_ns, path="/users")
api.add_namespace(inci_ns, path="/incidents")
