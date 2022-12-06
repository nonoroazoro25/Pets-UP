from . import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Boolean, nullable=True, default=True)
    pet_ids = db.Column(db.String(256), nullable=True)

    def to_basic_dict(self):
        resp_dict = {
            "id": self.id,
            "account": self.account,
            "password": self.password,
            "email": self.email,
            "status": self.status
        }
        return resp_dict
