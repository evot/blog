from . import *

from models import Comment
from models import Reply
from models import User
from utils import login_required
from utils import handle_upload
from utils import log

main = Blueprint('api', __name__)


# 处理注册请求
@main.route('/register', methods=['POST'])
def register():
    form = request.json
    r = User.register_validation(form)
    log(form, r)
    if r.get('success'):
        u = User(form)
        u.save()
        r['next'] = request.args.get('next', url_for('auth.index'))
        session['user_id'] = u.id
    return jsonify(r)


# 处理登陆请求
@main.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    r = User.login_validation(form)
    if r.get('success'):
        r['next'] = request.args.get('next', url_for('auth.index'))
        username = form.get('username')
        user = User.user_by_name(username)
        session['user_id'] = user.id
        # session.permanent = True
    return jsonify(r)


# 游客访问
@main.route('/visitor', methods=['POST'])
def visitor():
    session['user_id'] = 2
    r = {
        'success': True,
        'message': '匿名身份获取成功!',
        'next': url_for('auth.index'),
    }
    return jsonify(r)


@main.route('/comment/add', methods=['POST'])
def add_comment():
    form = request.json
    r = Comment.validation(form)
    if r.get('success'):
        c = Comment.new(form)
        r['data'] = c.json
        r['data']['csrf_token'] = form.get('csrf_token', '')
    return jsonify(r)


@main.route('/comment/<int:comment_id>/upvote')
def upvote_comment(comment_id):
    c = Comment.query.get(comment_id)
    if c:
        r = c.upvote_validation()
        return jsonify(r)
    else:
        abort(403)


@main.route('/comment/<int:comment_id>/delete')
def delete_comment(comment_id):
    c = Comment.query.get(comment_id)
    if c:
        r = c.delete_validation()
        return jsonify(r)
    else:
        abort(403)


@main.route('/reply/add', methods=['POST'])
def add_reply():
    form = request.json
    r = Reply.validation(form)
    if r.get('success'):
        reply = Reply.new(form)
        r['data'] = reply.json
    return jsonify(r)


@main.route('/reply/<int:reply_id>/upvote')
def upvote_reply(reply_id):
    reply = Reply.query.get(reply_id)
    if reply:
        r = reply.upvote_validation()
        return jsonify(r)
    else:
        abort(403)


@main.route('/reply/<int:reply_id>/delete')
def delete_reply(reply_id):
    reply = Reply.query.get(reply_id)
    if reply:
        r = reply.delete_validation()
        return jsonify(r)
    else:
        abort(403)


@main.route('/user/<int:user_id>/follow')
def follow(user_id):
    r = User.follow_validation(user_id)
    return jsonify(r)


def generic_upload(file, type):
    r = handle_upload(file, type)
    log(r)
    ok = r.get('success')
    message = r.get('message', '')
    script_head = '<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction(2,'
    script_tail = ');</script>'
    if ok:
        url = '/static/uploads/' + type + 's/' + r.get('new_filename')
        log(url)
        return script_head + '"' + url + '"' + script_tail
    else:
        return script_head + '""' + ',' + '"' + message + '"' + script_tail


@main.route('/upload/image', methods=['POST'])
@login_required
def upload_image():
    return generic_upload(request.files['upload'], 'image')


@main.route('/upload/file', methods=['POST'])
@login_required
def upload_file():
    return generic_upload(request.files['upload'], 'file')
