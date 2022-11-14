from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from common.utils.param_verify import verify_int_type
from common.models.user import User
from common.models import db


class UserResource(Resource):

    def get(self):
        """
        获取用户列表
        查询用户
        :return:
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('account', required=False, type=verify_int_type, location='args')
        qs_parser.add_argument('email', required=False, location='args')
        args = qs_parser.parse_args()
        account = args.account
        email = args.email

