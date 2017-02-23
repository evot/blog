from . import db

user_categories = db.Table('user_categories',
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
                           )
