import time

from flask import Markup
from utils import sanitize

from . import db
from . import ModelMixin


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.Integer, default=int(time.time()))
    view_count = db.Column(db.Integer, default=0)
    category_id = db.Column('Category', db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')

    def __init__(self, form):
        self.created_time = int(time.time())
        self.title = sanitize(form.get('title'))
        self.body = form.get('content')
        # self.body = sanitize(form.get('content'))

    @classmethod
    def show(cls, blog_id):
        b = Blog.valid_id(blog_id)
        if b:
            b.view_count += 1
            b.save()
            r = True
        else:
            r = False
        return r, b

    def _update(self, form):
        self.created_time = int(time.time())
        self.title = sanitize(form.get('title'))
        self.body = form.get('content')
        self.save()

    def extra_dict(self):
        d = dict(
            type=self.__class__.__name__,
            author_id=self.author_id,
            comments=self.comments,
        )
        return d

    def comment_count(self):
        return self.comments.count()

    @property
    def ordered_comments(self):
        return self.comments.order_by('created_time').all() or 0
