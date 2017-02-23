import time
from flask import g

from . import db
from . import ModelMixin

comment_upvotes = db.Table('comment_upvotes',
                           db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'), primary_key=True),
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                           )


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=int(time.time()))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    upvote_count = db.Column(db.Integer, default=0)
    replies = db.relationship('Reply', backref='comment', lazy='dynamic')
    upvote_users = db.relationship('User',
                                   secondary=comment_upvotes,
                                   backref=db.backref('upvote_comments'),
                                   )

    def __init__(self, form):
        self.created_time = int(time.time())
        self.content = form.get('content', '')
        self.sender_id = form.get('sid', 0)
        self.receiver_id = form.get('rid', 0)
        self.blog_id = form.get('bid', 0)

    def extra_dict(self):
        d = dict(
            type=self.__class__.__name__,
            sender_profile=self.sender.profile_link(),
            receiver_profile=self.receiver.profile_link(),
            sender_name=self.sender.username,
            receiver_name=self.receiver.username,
            blog_id=self.blog_id,
            formatted_time=self.format_time(self.created_time),
            is_upvoted=self.is_upvoted,
            reply_count=self.reply_count,
        )
        return d

    @property
    def json(self):
        black_list = ['sender', 'receiver']
        return self.data_dict(black_list=black_list)

    @staticmethod
    def validation(form):
        r = {
            'success': False
        }
        content = form.get('content', '')
        if not g.user:
            r['message'] = '登录后才能评论'
        else:
            if len(content) > 0:
                r['success'] = True
            else:
                r['message'] = '评论不能为空'
        return r

    @property
    def is_upvoted(self):
        u = g.user
        r = u in self.upvote_users
        return r

    def upvote_validation(self):
        r = {
            'success': False,
        }
        u = g.user
        if u:
            if u in self.upvote_users:
                self.upvote_users.remove(u)
                self.upvote_count -= 1
                self.save()
                r['success'] = True
                r['message'] = '取消点赞成功'
                r['upvote'] = False
                r['cancel_upvote'] = True
            else:
                self.upvote_users.append(u)
                self.upvote_count += 1
                self.save()
                r['success'] = True
                r['message'] = '点赞成功'
                r['upvote'] = True
                r['cancel_upvote'] = False
        else:
            r['message'] = '登录后才能点赞'
        return r

    def reply_validation(self):
        r = {
            'success': False,
        }
        u = g.user
        if u:
            self.reply_count += 1
            self.save()
            r['success'] = True
            r['message'] = '回复成功'
        else:
            r['message'] = '登录后才能回复'
        print('回复 返回的 r 和 c ', r, self)
        return r

    def delete_validation(self):
        r = {
            'success': False,
        }
        if g.user.id == self.sender_id:
            self.delete(self.id)
            r['success'] = True
            r['message'] = '删除成功'
        return r

    @property
    def ordered_replies(self):
        return self.replies.order_by('created_time').all()

    @property
    def reply_count(self):
        return self.replies.count()
