from . import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    create_time = db.Column('create_time', db.DateTime, default=datetime.now(), doc='创建时间')
    update_time = db.Column('update_time', db.DateTime, default=datetime.now(), onupdate=datetime.now, doc='更新时间')
