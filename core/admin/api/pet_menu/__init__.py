from flask import Blueprint
from flask_restful import Api
from core.admin.api.pet_menu import pet_menu

menu_bp = Blueprint('menu', __name__)
menu_api = Api(menu_bp)

menu_api.add_resource(pet_menu.MenuResource, '/api/pet/menu', endpoint='PetMenu')