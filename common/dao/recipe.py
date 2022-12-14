from flask import current_app
from common.models import db
from common.models.recipe import Recipe
from common.errors.base_exception import DatabaseError


def get_recipe_all():
    try:
        info = Recipe.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def get_recipe_by_id(recipe_id):
    try:
        info = Recipe.query.get(recipe_id)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def delete_recipe_by_args(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if recipe is None:
        return False
    else:
        db.session.delete(recipe)
        db.session.commit()
    return True


def update_recipe_info_by_id(recipe_id, kwargs):
    try:
        Recipe.query.filter_by(id=recipe_id).update(kwargs)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True