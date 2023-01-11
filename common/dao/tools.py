from flask import current_app
from common.models import db
from common.models.tools import Tag, Deworm
from common.errors.base_exception import DatabaseError


def get_tag_all():
    try:
        info = Tag.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def get_tag_by_id(tag_id):
    try:
        info = Tag.query.get(tag_id)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def delete_tag_by_args(tag_id):
    tag = get_tag_by_id(tag_id)
    if tag is None:
        return False
    else:
        db.session.delete(tag)
        db.session.commit()
    return True


def update_tag_info_by_id(tag_id, kwargs):
    try:
        Tag.query.filter_by(id=tag_id).update(kwargs)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True


def get_deworm_all():
    try:
        info = Deworm.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def get_deworm_by_id(deworm_id):
    try:
        info = Deworm.query.get(deworm_id)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def delete_deworm_by_args(deworm_id):
    deworm = get_deworm_by_id(deworm_id)
    if deworm is None:
        return False
    else:
        db.session.delete(deworm)
        db.session.commit()
    return True


def update_deworm_info_by_id(deworm_id, kwargs):
    try:
        Deworm.query.filter_by(id=deworm_id).update(kwargs)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True