from . import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
