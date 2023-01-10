from . import db
from .base import BaseModel


class Purchase(BaseModel):
    __tablename__ = 'tb_purchase'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(256))
    brand = db.Column(db.Float)
    nutrient_content = db.Column(db.DateTime)       # 营养成分
    validity_period = db.Column(db.String(256))     # 有效期
    photo = db.Column(db.String(256))
    open_time = db.Column(db.DateTime)              # 开启时间
    total_use_time = db.Column(db.Integer)
    love_degree = db.Column(db.String(256))

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "type": self.type,
            "brand": self.brand,
            "nutrient_content": self.nutrient_content,
            "open_time": self.open_time,
            "total_use_time": self.total_use_time,
            "love_degree": self.love_degree,
        }
        return resp_data