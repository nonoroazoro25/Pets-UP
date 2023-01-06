from . import db
from .base import BaseModel


class Pet(BaseModel):
    __tablename__ = 'tb_pet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(256))
    type = db.Column(db.String(256))
    photo = db.Column(db.LargeBinary(length=2048))

    def to_basic_dict(self):
        resp_dic = {
            "id": self.id,
            "name": self.name,
            "type": self.type
        }
        return resp_dic


class PetRecord(BaseModel):
    __tablename__ = 'tb_pet_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer)
    title = db.Column(db.String(256))
    photo = db.Column(db.String(256))
    detail = db.Column(db.String(256))
    weight = db.Column(db.Float)
    tag = db.Column(db.String(256))

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "pet_id": self.pet_id,
            "title": self.title,
            "detail": self.detail,
            "weight": self.weight,
            "tag": self.tag
        }
        return resp_data
