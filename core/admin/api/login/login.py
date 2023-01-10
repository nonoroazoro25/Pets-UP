import time
from datetime import datetime, timedelta
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from flask import current_app, g
from common.utils.response_util import response_to_api
from common.dao.user import get_user_by_user_name
from common.utils.jwt_util import generate_jwt


class LoginResource(Resource):
    """
    登录接口
    """

    def _generate_tokens(self, user_id, account, refresh=True):
        """
        生成token 和refresh_token
        :param user_id: 用户id
        :return: token, refresh_token
        """
        # 颁发JWT
        secret = current_app.config['JWT_SECRET']
        # 生成调用token， refresh_token
        expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
        current_heart_time = int(time.time())
        token = generate_jwt(
            {'user_id': user_id, "account": account,
             "current_heart_time": current_heart_time}, expiry,
            secret)

        if refresh:
            exipry = datetime.utcnow() + timedelta(days=current_app.config['JWT_REFRESH_DAYS'])
            refresh_token = generate_jwt(
                {'user_id': user_id, "account": account, 'is_refresh': True,
                 "current_heart_time": current_heart_time}, exipry,
                secret)
        else:
            refresh_token = None

        return token, refresh_token

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
        account = args.username
        password = args.password
        response_data = {}

        database_user = get_user_by_user_name(account)
        if not database_user:
            return response_to_api(code=601, data=response_data)
        user_id = database_user.id

        if password != database_user.password:
            return response_to_api(code=602, data=response_data)
        token, refresh_token = self._generate_tokens(user_id, account)
        response_data['detail'] = database_user.to_basic_dict()
        response_data["token"] = token
        response_data["refresh_token"] = refresh_token
        return response_to_api(code=0, data=response_data)

    def options(self):
        pass


class LogoutResource(Resource):
    """
    注销
    """

    def post(self):
        pass



