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