from flask import Blueprint
from flask_restful import Api
from core.admin.api.material import material

recipe_bp = Blueprint('recipe', __name__)
recipe_api = Api(recipe_bp)

recipe_api.add_resource(material.MaterialResource, '/api/material/list', endpoint='MaterialList')
recipe_api.add_resource(material.MaterialResource, '/api/material/create', endpoint='MaterialCreate')
