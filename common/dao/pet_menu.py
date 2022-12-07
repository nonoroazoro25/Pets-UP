from flask import current_app
from common.models import db
from common.models.pets_menu import PetMenu
from common.errors.base_exception import DatabaseError


def get_menu_all():
    try:
        info = PetMenu.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info
