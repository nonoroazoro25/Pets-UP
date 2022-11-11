# _*_ coding:UTF-8


class Configure(object):

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.host = '0.0.0.0'
        self.port = '8090'
        self.auth_protocol = 'http'
        self.web_mode = "product"  # 运行模式


def get_config():
    config = Configure()
    return config
