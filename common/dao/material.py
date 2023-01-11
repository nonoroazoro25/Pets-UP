from flask import current_app
from common.models import db
from common.models.recipe import RawMaterial
from common.errors.base_exception import DatabaseError


def get_material_all():
    try:
        info = RawMaterial.query.all()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def get_material_by_id(material_id):
    try:
        info = RawMaterial.query.get(material_id)
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return info


def delete_material_by_args(material_id):
    material = get_material_by_id(material_id)
    if material is None:
        return False
    else:
        db.session.delete(material)
        db.session.commit()
    return True


def update_material_info_by_id(material_id, kwargs):
    try:
        RawMaterial.query.filter_by(id=material_id).update(kwargs)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        raise DatabaseError
    return True