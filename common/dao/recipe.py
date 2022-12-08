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