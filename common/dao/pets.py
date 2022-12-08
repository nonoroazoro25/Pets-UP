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


def get_pet_by_user_id(user_id):
    try:
        info = Pet.query.filter_by(user_id=user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def update_pet_name_by_pet_id(pet_id, update_dict):
    try:
        Pet.query.filter_by(id=pet_id).update(update_dict)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return False
    return True


def delete_pet_by_pet_id(pet_id):
    try:
        Pet.query.filter_by(id=pet_id).delete()
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True