from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from common.models import db
from flask import current_app, g
from common.utils.response_util import response_to_api


class MenuResource(Resource):
    def get(self):
        print('get menu')
        pass