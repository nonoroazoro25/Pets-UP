import os


class Config(object):
    ERROR_404_HELP = False

    # 默认csrf保护  false
    WTF_CSRF_CHECK_DEFAULT = False

    # 显示生成的sql 语句
    SQLALCHEMY_ECHO = True

    # JWT
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
    JWT_EXPIRY_HOURS = 1
    JWT_REFRESH_DAYS = 14

    # mysql
    SQLALCHEMY_DATABASE_URI = " "


# 开发环境配置信息
class DevelopmentConfig(Config):
    pass


# 生产环境配置信息(线上)
class ProductConfig(Config):
    DEBUG = False
    # 设置默认日志级别
    LOGGING_LEVEL = 'INFO'
    SQLALCHEMY_ECHO = False


# 测试环境配置信息
class TestingConfig(Config):
    TESTING = True


# 通过字典统一访问配置类
config_dict = {
    "development": DevelopmentConfig,
    "product": ProductConfig,
    "testing": TestingConfig,
}