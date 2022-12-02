from flask import Blueprint
from flask_restful import Api
from core.admin.api.pets import pets

pets_bp = Blueprint('pets', __name__)
pets_api = Api(pets_bp)

pets_api.add_resource(pets.PetsResource, '/api/pets/list', endpoint='PetsList')
pets_api.add_resource(pets.PetsResource, '/api/pets/create', endpoint='PetsListCreate')