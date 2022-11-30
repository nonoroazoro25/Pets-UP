import os
from flask import Flask, send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_apidoc import ApiDoc
from common.models import db

DIST_PATH = ""


def create_flask_app(config):
    _app = Flask(__name__, static_folder=DIST_PATH, static_url_path="")
    _app.config.from_object(config)
    return _app


def create_app(config_name):
    from core.admin.settings.views import config_dict
    config = config_dict.get(config_name)
    # 创建m_app对象
    m_app = create_flask_app(config)
    # 定时任务
    # m_app.config.from_object()

    # 数据库初始化
    db.init_app(m_app)

    # 请求钩子

    # 初始化session
    # Session()

    # 设置csrf
    CSRFProtect(m_app)

    # 设置跨域
    CORS(m_app, supports_credentials=True, resource=r'/*')

    # 注册蓝图
    from core.admin.api.user import user_bp
    m_app.register_blueprint(user_bp)

    m_app.app_context().push()
    ApiDoc(m_app)
