from . import *

from models import Blog
from models import User
from utils import log

main = Blueprint('auth', __name__)


# 请求首页
@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    blog_pagination = Blog.query.order_by(Blog.created_time.desc()).paginate(page=page, per_page=per_page)
    kwargs = dict(
        pagination=blog_pagination,
        endpoint='auth.index',
    )
    return render_template('index.html', **kwargs)


# 显示登录和注册界面的函数  GET
@main.route('/login')
def login_view():
    return render_template('login.html')


# 注销
@main.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('auth.index'))


@main.app_errorhandler(404)
def not_found(error):
    return render_template('not_found.html')


@main.app_errorhandler(405)
def not_found(error):
    return render_template('error.html')


@main.app_errorhandler(403)
def not_found(error):
    return render_template('error.html')
