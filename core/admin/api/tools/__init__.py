from flask import Blueprint
from flask_restful import Api
from core.admin.api.tools import tag, deworm

tools_bp = Blueprint('tools', __name__)
tools_api = Api(tools_bp)

tools_api.add_resource(tag.TagResource, '/api/tag/list', endpoint='TagListResource')
tools_api.add_resource(tag.TagResource, '/api/tag/create', endpoint='TagCreateResource')

tools_api.add_resource(deworm.DewormResource, '/api/deworm/list', endpoint='DewormListResource')
tools_api.add_resource(deworm.DewormResource, '/api/deworm/create', endpoint='DewormCreateResource')
