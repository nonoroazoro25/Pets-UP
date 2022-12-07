from flask import Blueprint
from flask_restful import Api
from core.admin.api.login import login

login_bp = Blueprint('login', __name__)
login_api = Api(login_bp)

login_api.add_resource(login.LoginResource, '/api/login', endpoint='LoginResource')