from flask import Blueprint
from flask_restful import Api
from core.admin.api.pets import pets
from core.admin.api.pets import pet_record

pets_bp = Blueprint('pets', __name__)
pets_api = Api(pets_bp)

# 宠物
pets_api.add_resource(pets.PetsResource, '/api/pets/list', endpoint='PetsList')
pets_api.add_resource(pets.PetsResource, '/api/pets/create', endpoint='PetsListCreate')

# 宠物记录
pets_api.add_resource(pet_record.PetsRecordResource, '/api/pets/record/list', endpoint='PetsRecordList')
pets_api.add_resource(pet_record.PetsRecordResource, '/api/pets/record/create', endpoint='PetsRecordCreate')