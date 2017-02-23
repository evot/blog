from . import *
from flask import flash
from models import ImageStore
from models import User
from utils import log
from utils import login_required
from utils import handle_upload

main = Blueprint('user', __name__)


# 请求用户资料页面
@main.route('/<int:user_id>/profile')
def profile(user_id):
    u = User.query.get(user_id)
    if u:
        return render_template('profile.html', user=u)
    else:
        abort(404)


@main.route('/<int:user_id>/profile/edit')
def edit_profile_view(user_id):
    u = User.query.get(user_id)
    if not u:
        abort(404)
    elif u != g.user:
        abort(403)
    else:
        return render_template('profile_edit.html', user=u)


@main.route('/<int:user_id>/profile/edit', methods=['POST'])
def edit_profile(user_id):
    u = User.query.get(user_id)
    if not u:
        abort(404)
    elif u != g.user:
        abort(403)
    else:
        form = request.form
        log(form)
        messages = []
        r = u.profile_validation(form)
        if not r.get('success'):
            for message in r.get('message', []):
                messages.append(message)

        if request.files.get('avatar'):
            avatar = request.files['avatar']
            upload_info = handle_upload(avatar, 'image')
            log(avatar, upload_info)

            if upload_info.get('success'):
                img = ImageStore(upload_info['old_filename'], upload_info['new_filename'])
                img.save()
                u.set_avatar(upload_info['new_filename'])
            else:
                # errors.append("Avatar upload failed")
                messages.append(upload_info['message'])
        if messages:
            return render_template('profile_edit.html', user=u, messages=messages)
        else:
            messages.append('修改成功')

            return redirect(url_for('.edit_profile_view', user_id=user_id))


@main.route('/<int:user_id>/follows')
def follows(user_id):
    u = User.query.get(user_id)
    if not u:
        abort(404)
    else:
        return render_template('follows.html', user=u)
