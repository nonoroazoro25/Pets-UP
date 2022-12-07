from flask import Blueprint
from flask_restful import Api
from core.admin.api.user import user

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

user_api.add_resource(user.UserResource, '/api/user/list', endpoint='UserList')

user_api.add_resource(user.UserResource, '/api/user/create', endpoint='UserListCreate')

user_api.add_resource(user.UserInfoResource, '/api/user/info', endpoint='UserInfo')
