from flask import Blueprint
from flask_restful import Api
from core.admin.api.recipe import recipe

recipe_bp = Blueprint('recipe', __name__)
recipe_api = Api(recipe_bp)

recipe_api.add_resource(recipe.RecipeResource, '/api/recipe/list', endpoint='RecipeList')
recipe_api.add_resource(recipe.RecipeResource, '/api/recipe/create', endpoint='RecipeListCreate')
recipe_api.add_resource(recipe.RecipeResource, '/api/recipe/delete', endpoint='RecipeDelete')
recipe_api.add_resource(recipe.RecipeResource, '/api/recipe/update', endpoint='RecipeUpdate')