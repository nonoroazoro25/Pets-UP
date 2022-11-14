from . import db
from .base import BaseModel


class Recipe(BaseModel):
    __tablename__ = 'tb_recipe'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    weight = db.Column(db.Float)
    cook_time = db.Column(db.DateTime)
    remark = db.Column(db.String(256))
    photo = db.Column(db.String(256))


class RawMaterial(BaseModel):
    __tablename__ = 'tb_raw_material'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))

