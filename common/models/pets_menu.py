from . import db
from .base import BaseModel


class PetMenu(BaseModel):
    __tablename__ = "tb_pets_menu"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    menuId = db.Column(db.Integer)
    icon = db.Column(db.String(256))
    open = db.Column(db.Integer)
    orderNum = db.Column(db.Integer)
    parentId = db.Column(db.Integer)
    parentName = db.Column(db.String(256))
    perms = db.Column(db.String(256))
    type = db.Column(db.Integer)
    url = db.Column(db.String(256))

    def to_basic_dict(self):
        resp_data = {
            "id": self.id,
            "name": self.name,
            "menuId": self.menuId,
            "icon": self.icon,
            "open": self.open,
            "parentId": self.parentId,
            "orderNum": self.orderNum,
            "parentName": self.parentName,
        }
        return resp_data