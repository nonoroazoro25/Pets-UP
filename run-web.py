# -*- coding: UTF-8 -*-

from gevent import pywsgi
from core.admin import g_app

if __name__ == '__main__':
    server = pywsgi.WSGIServer(("0.0.0.0", 2020), g_app)
    server.serve_forever()
