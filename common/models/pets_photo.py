from . import db
from .base import BaseModel


class PetsPhoto(BaseModel):
    __tablename__ = 'tb_pets_photo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.String(256))

