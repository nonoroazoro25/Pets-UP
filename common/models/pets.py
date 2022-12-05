from . import db
from .base import BaseModel


class Pet(BaseModel):
    __tablename__ = 'tb_pet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    type = db.Column(db.String(256))

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
    title = db.Column(db.String(256))
    photo = db.Column(db.String(256))
    detail = db.Column(db.String(256))
    weight = db.Column(db.Float)
    tag = db.Column(db.String(256))
