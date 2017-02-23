import time

from . import db
from . import ModelMixin


class Follow(db.Model, ModelMixin):
    __tablename__ = 'follows'
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    to_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_time = db.Column(db.Integer, default=int(time.time()))

    def __init__(self, from_user, to_user):
        self.from_id = from_user.id
        self.to_id = to_user.id
        self.created_time = int(time.time())

    def __repr__(self):
        return u'<{}: from {} to {}>'.format(self.__class__.__name__, self.from_id, self.to_id)

    # 外键存在循环引用的问题， 需要额外添加
    def extra_dict(self):
        d = dict(
            type=self.__class__.__name__,
            from_id=self.from_id,
            to_id=self.to_id,
        )
        return d
