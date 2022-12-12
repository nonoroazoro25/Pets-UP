from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from flask import current_app, g
from common.utils.response_util import response_to_api


class LoginResource(Resource):
    """
    登录接口
    """

    def post(self):
        """
        @api {post} /api/license  激活license
        @apiVersion 1.0.0
        @apiName create license
        @apiGroup LicenseResource
        @apiHeader {String} Authorization token
        @apiParam {String}  license        (必须)  license
        @apiSuccess (回参) {String} license license
        @apiSuccessExample {json} Success-Response:
            {
                "code": 200,
                "value": "OK",
                "data": null,
                "result": true
            }
        @apiErrorExample {json} Error-Response:
            {
                "code": 4001,
                "value": "Account does not exist",
                "data": null,
                "result": false
            }
        """
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
