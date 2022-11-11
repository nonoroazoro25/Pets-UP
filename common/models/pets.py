from . import db
from .base import BaseModel


class Pet(BaseModel):
    __tablename__ = 'tb_pet'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    weight = db.Column(db.Float)
