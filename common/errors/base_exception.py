from http.client import HTTPException
from common.utils.response_util import response_to_api


class APIException(HTTPException):
    code = 400
    message = 'Sorry, there was an unexpected error'

    def __init__(self, msg=None, code=None, headers="application/json"):

        self.headers = headers
        if code:
            self.code = code
        if msg:
            self.message = msg
        super().__init__(msg, None)

    def get_body(self):
        return response_to_api(code=self.code, result=False)

    def get_headers(self):
        return [("Content-Type", self.headers)]


class DatabaseError(APIException):
    code = 1001
    message = '数据库异常'
