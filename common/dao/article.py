from flask import current_app
from common.models import db
from common.models.pets_article import PetsArticle
from common.errors.base_exception import DatabaseError


def get_article_all():
    try:
        info = PetsArticle.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def get_article_by_id(article_id):
    try:
        info = PetsArticle.query.get(article_id)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def delete_article_by_args(article_id):
    material = get_article_by_id(article_id)
    if material is None:
        return False
    else:
        db.session.delete(material)
        db.session.commit()
    return True


def update_article_info_by_id(article_id, kwargs):
    try:
        PetsArticle.query.filter_by(id=article_id).update(kwargs)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True