from . import db
from .base import BaseModel


class Tag(BaseModel):
    __tablename__ = 'tb_tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(256))
