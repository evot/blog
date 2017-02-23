import time

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import g

from . import db
from . import ModelMixin
from .follow import Follow
from .categories import user_categories


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    hashed_password = db.Column(db.String(60))
    gender = db.Column(db.String(10))
    note = db.Column(db.String(255))
    _avatar = db.Column(db.String(100))
    role = db.Column(db.Integer, default=2)
    created_time = db.Column(db.Integer, default=0)
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')

    sent_comments = db.relationship('Comment', foreign_keys='Comment.sender_id', backref='sender', lazy='dynamic')
    received_comments = db.relationship('Comment', foreign_keys='Comment.receiver_id', backref='receiver',
                                        lazy='dynamic')

    sent_replies = db.relationship('Reply', foreign_keys='Reply.sender_id', backref='sender', lazy='dynamic')
    received_replies = db.relationship('Reply', foreign_keys='Reply.receiver_id', backref='receiver',
                                       lazy='dynamic')

    followed_follows = db.relationship('Follow', foreign_keys='Follow.from_id',
                                       backref=db.backref('follower', lazy='joined'),
                                       lazy='dynamic', cascade='all, delete-orphan')
    follower_follows = db.relationship('Follow', foreign_keys='Follow.to_id',
                                       backref=db.backref('followed_user', lazy='joined'),
                                       lazy='dynamic', cascade='all, delete-orphan')
    categories = db.relationship('Category',
                                 secondary=user_categories,
                                 backref=db.backref('users', lazy='dynamic'),
                                 lazy='dynamic')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username')
        self.gender = form.get('gender')
        self.note = form.get('note')
        self.created_time = int(time.time())
        self.password = form.get('password', '')

    def extra_dict(self):
        d = dict(
            type=self.__class__.__name__,
            blogs=self.blogs,
            sent_comments=self.sent_comments,
            received_comments=self.received_comments,
            followed_follows=self.followed_follows,
            follower_follows=self.follower_follows,
            categories=self.categories,
        )
        return d

    def is_admin(self):
        return self.role == 1

    # def is_guest(self):
    #     return self.role == 3

    @property
    def avatar(self):
        if self._avatar:
            return '/static/uploads/images/' + self._avatar
        return '/static/images/avatar.jpg'

    def set_avatar(self, avatar):
        self._avatar = avatar
        self.save()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def _update(self, form):
        print('user.update, ', form)
        self.password = form.get('password', self.password)

    @classmethod
    def user_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def is_legal_name(cls, username):
        name_info = {
            'is_not_exists': False,
            'is_length_ok': False,
        }
        if not cls.user_by_name(username):
            name_info['is_not_exists'] = True
        user_name_len = len(username)
        if user_name_len >= 3:
            name_info['is_length_ok'] = True
        return name_info

    @staticmethod
    def is_legal_pwd(password):
        password_info = {
            'is_length_ok': False,
        }
        if len(password) >= 3:
            password_info['is_length_ok'] = True
        return password_info

    @classmethod
    def register_validation(cls, form):
        r = {
            'success': False,
        }
        username = form.get('username', '')
        password = form.get('password', '')
        name_info = cls.is_legal_name(username)
        password_info = cls.is_legal_pwd(password)
        r['name_info'] = name_info
        r['password_info'] = password_info
        if username and password:
            valid_username = all(value for value in name_info.values())
            valid_password = all(value for value in password_info.values())
            if valid_username and valid_password:
                r['success'] = True
            elif not valid_password:
                r['message'] = '密码长度不能小于3!'
            else:
                r['message'] = '注册失败！'
        else:
            r['message'] = '用户名和密码不能为空！'
        return r

    @classmethod
    def login_validation(cls, form):
        r = {
            'success': False,
            'message': '登录失败！'
        }
        username = form.get('username', '')
        password = form.get('password', '')
        name_info = cls.is_legal_name(username)
        user = cls.user_by_name(username)
        r['name_info'] = name_info
        if user:
            if password and username:
                username_equals = username == user.username
                password_equals = user.verify_password(password)
                if username_equals and password_equals:
                    r['success'] = True
                    r['message'] = '登录成功！'
                else:
                    r['message'] = '用户名或密码错误！'
            else:
                r['message'] = '用户名和密码不能为空！'
        return r

    def profile_validation(self, form):
        r = {
            'success': False,
            'message': [],
        }
        username = form.get('username', '')
        name_info = User.is_legal_name(username)
        valid_username_a = all(value for value in name_info.values())
        valid_username_b = (self.username == username) and name_info['is_length_ok']
        valid_username = valid_username_a or valid_username_b

        gender = form.get('gender', '').strip()
        valid_gender = gender in ('男', '女', '')
        if not valid_gender:
            r['message'].append('性别只能为男或女')
        if not name_info['is_length_ok']:
            r['message'].append('用户名长度不得小于3')
        if not name_info['is_not_exists'] and username != self.username:
            r['message'].append('用户名已存在')
        if valid_username and valid_gender:
            r['success'] = True
            self.gender = gender
            self.note = form.get('note', '')
            self.username = username
            self.save()
        return r

    def profile_link(self):
        return '/user/' + str(self.id) + '/profile'

    @staticmethod
    def follow_validation(user_id):
        r = {
            'success': False,
        }
        user = User.query.get(user_id)
        current_user = g.user
        if not current_user:
            r['message'] = '登录后才能执行此操作'
            return r
        if user and (user is not current_user):
            if not current_user.is_following(user):
                current_user.follow(user)
                r['success'] = True
                r['message'] = '关注成功'
                r['follow'] = True
                r['unfollow'] = False

            else:
                current_user.unfollow(user)
                r['success'] = True
                r['message'] = '取关成功'
                r['follow'] = False
                r['unfollow'] = True
        return r

    def follow(self, user):
        r = False
        if not self.is_following(user):
            f = Follow(self, user)
            f.save()
            r = True
        return r

    def unfollow(self, user):
        f = self.followed_follows.filter_by(to_id=user.id).first()
        if f:
            f.remove()

    def is_following(self, user):
        return self.followed_follows.filter_by(to_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.follower_follows.filter_by(from_id=user.id).first() is not None

    @property
    def following_count(self):
        return len(self.followed_follows.all())

    @property
    def follower_count(self):
        return len(self.follower_follows.all())

    @property
    def blog_count(self):
        return self.blogs.count()

    @property
    def followed_users(self):
        followed_users = []
        for follow in self.followed_follows.filter_by(from_id=self.id).all():
            followed_users.append(follow.followed_user)
        return followed_users

    @property
    def followers(self):
        followers = []
        for follow in self.follower_follows.filter_by(to_id=self.id).all():
            followers.append(follow.follower)
        return followers
