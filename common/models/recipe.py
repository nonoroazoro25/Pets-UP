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

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "name": self.name,
            "weight": self.weight,
            "cook_time": self.cook_time,
            "remark": self.remark,
        }
        return resp_data


class RawMaterial(BaseModel):
    __tablename__ = 'tb_raw_material'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    nutrient_content = db.Column(db.String(256))  # 营养成分表
    matchable = db.Column(db.String(256))

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "name": self.name,
            "nutrient_content": self.nutrient_content,
            "matchable": self.matchable
        }
        return resp_data

