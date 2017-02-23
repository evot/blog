import time
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModelMixin(object):
    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def valid_id(cls, model_id):
        return cls.query.get(model_id)

    @classmethod
    def update(cls, model_id, form):
        m = cls.valid_id(model_id)
        if m:
            m._update(form)
            m.save()
            r = True
        else:
            r = False
        return r, m

    @classmethod
    def delete(cls, model_id):
        if cls.valid_id(model_id):
            m = cls.query.get(model_id)
            m.remove()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def data_dict(self, white_list=[], black_list=[]):
        extra_dict = self.extra_dict()
        black_list = self.black_list() + black_list
        d = {k: v for k, v in self.__dict__.items()}
        d.update(extra_dict)
        for b in black_list:
            del d[b]
        # print(type(list(d.keys())))
        if white_list:
            for key in list(d.keys()):
                if key not in white_list:
                    del d[key]
        return d

    def format_time(self, timestamp):
        t = time.localtime(timestamp)
        time_format = '%Y-%m-%d %H:%M'
        ft = time.strftime(time_format, t)
        return ft

    def extra_dict(self):
        raise NotImplementedError

    def black_list(self):
        b = [
            '_sa_instance_state',
        ]
        return b


from .blog import Blog
from .user import User
from .comment import Comment
from .reply import Reply
from .follow import Follow
from .category import Category
from .categories import user_categories
from .image import ImageStore
