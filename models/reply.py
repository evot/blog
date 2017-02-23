import time
from flask import g

from . import db
from . import ModelMixin

reply_upvotes = db.Table('reply_upvotes',
                         db.Column('reply_id', db.Integer, db.ForeignKey('replies.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                         )


class Reply(db.Model, ModelMixin):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=int(time.time()))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    upvote_count = db.Column(db.Integer, default=0)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    upvote_users = db.relationship('User',
                                   secondary=reply_upvotes,
                                   backref=db.backref('upvote_replies'),
                                   )

    def __init__(self, form):
        self.created_time = int(time.time())
        self.content = form.get('content', '')
        self.sender_id = g.user.id
        self.receiver_id = form.get('rid', 0)
        self.comment_id = form.get('cid', 0)

    def extra_dict(self):
        d = dict(
            type=self.__class__.__name__,
            sender_profile=self.sender.profile_link(),
            receiver_profile=self.receiver.profile_link(),
            sender_name=self.sender.username,
            receiver_name=self.receiver.username,
            comment_id=self.comment_id,
            formatted_time=self.format_time(self.created_time),
            is_upvoted=self.is_upvoted,
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
