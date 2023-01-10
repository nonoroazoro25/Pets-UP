from . import db
from .base import BaseModel


class PetsArticle(BaseModel):
    __tablename__ = 'tb_pets_article'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    pet_id = db.Column(db.Integer)
    title = db.Column(db.String(256))
    content = db.Column(db.String(256))    # 需要是富文本

    def to_basic_dict(self):
        resp_data = {
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'pet_id': self.pet_id
        }
        return resp_data

