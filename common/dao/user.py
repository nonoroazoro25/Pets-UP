from flask import current_app
from common.models import db
from common.models.user import User
from common.errors.base_exception import DatabaseError


def get_user_all():
    try:
        info = User.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def get_user_by_user_id(user_id):
    try:
        info = User.query.filter_by(id=user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def update_user_by_user_id(user_id, update_dict):
    try:
        User.query.filter_by(id=user_id).update(update_dict)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return False
    return True


def delete_user_by_user_id(user_id):
    try:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True
