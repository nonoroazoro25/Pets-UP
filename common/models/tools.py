from . import db
from .base import BaseModel


class Tag(BaseModel):
    __tablename__ = 'tb_tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(256))

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "type": self.type,
        }
        return resp_data


class Deworm(BaseModel):
    __tablename__ = 'tb_deworm'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    remark = db.Column(db.String(256))

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "remark": self.remark,
        }
        return resp_data
