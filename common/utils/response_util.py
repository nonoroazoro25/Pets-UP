from common.constants.response_code import ResultCode


def decode_result(code):
    if code not in ResultCode:
        return ''
    return ResultCode[code]


def response_to_api(code=None, msg=True, data=None):
    if code != 200:
        msg = decode_result(code)
    return {"code": code, "msg": msg, "data": data}
