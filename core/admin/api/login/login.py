from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from flask import current_app, g
from common.utils.response_util import response_to_api


class LoginResource(Resource):
    """
    登录接口
    """

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('username', required=True, location='json')
        json_parser.add_argument('password', required=True, location='json')
        args = json_parser.parse_args()

        response_data = {
            "expire": 43200,
            "token": "bf23308b3f67091abd49c071123bdff7"
        }


        return response_to_api(code=0, data=response_data)

    def options(self):
        pass
