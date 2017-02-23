import time
from flask import g

from . import db


class ImageStore(db.Model):
    __tablename__ = 'image_store'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    filename = db.Column(db.String(256))
    upload_time = db.Column(db.Integer, default=int(time.time()))
    stored_filename = db.Column(db.String(80), unique=True)

    author = db.relationship('User', foreign_keys='ImageStore.user_id', uselist=False)

    def __init__(self, filename, stored_filename):
        author = g.user
        if author:
            self.author = author
            self.filename = filename
            self.stored_filename = stored_filename

    def save(self):
        db.session.add(self)
        db.session.commit()
