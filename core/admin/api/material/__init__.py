from flask import Blueprint
from flask_restful import Api
from core.admin.api.material import material

material_bp = Blueprint('material', __name__)
material_api = Api(material_bp)

material_api.add_resource(material.MaterialResource, '/api/material/list', endpoint='MaterialList')
material_api.add_resource(material.MaterialResource, '/api/material/create', endpoint='MaterialCreate')
