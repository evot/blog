from . import *

from models import Blog
from utils import login_required
from utils import log
from models import User

main = Blueprint('blog', __name__)


# 添加博客页面
@main.route('/add')
@login_required
def add_view():
    return render_template('blog_add.html')


@main.route('/add', methods=['POST'])
@login_required
def add():
    u = g.user
    form = request.form
    b = Blog(form)
    b.author = u
    b.save()
    return redirect(url_for('auth.index'))


# 博客正文显示
@main.route('/<int:blog_id>')
def blog_view(blog_id):
    r, b = Blog.show(blog_id)
    if r:
        return render_template('blog.html', blog=b)
    else:
        abort(404)


# 编辑博客页面
@main.route('/edit/<int:blog_id>')
@login_required
def edit_view(blog_id):
    b = Blog.query.get(blog_id)
    return render_template('blog_edit.html', blog=b)


# 修改博客
@main.route('/update/<int:blog_id>', methods=['POST'])
@login_required
def update(blog_id):
    form = request.form
    r, b = Blog.update(blog_id, form)
    if r:
        return redirect(url_for('auth.index'))
    else:
        abort(404)
