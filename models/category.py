import time

from . import db
from . import ModelMixin


class Category(db.Model, ModelMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    created_time = db.Column(db.Integer, default=int(time.time()))
    blogs = db.relationship('Blog', backref='category', lazy='dynamic')

    def __init__(self):
        pass

    def extra_dict(self):
        d = dict(
            type=self.__class__.__name__,
            blogs=self.blogs,
        )
        return d
