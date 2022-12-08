from flask import current_app
from common.models import db
from common.models.pets import Pet
from common.errors.base_exception import DatabaseError


def get_pet_all():
    try:
        info = Pet.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info