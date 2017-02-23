from flask import Flask
from flask import request
from flask import abort
from flask import session
from flask import g
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from utils import log
from utils import from_now, short_time, format_time
from utils import gen_csrf_token
from utils import text_abstract

from models import db

from models import User
from models import Blog
from models import Comment
from models import Follow
from models import Category
from models import user_categories

app = Flask(__name__)
manager = Manager(app)


def configured_app():
    app.config.from_object('config')
    # 初始化 db
    db.init_app(app)
    # 注册路由
    register_routes(app)
    configure_env_vars(app)
    # 返回配置好的 app 实例
    return app


def configure_manager():
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def register_routes(app):
    """
    在这个函数里面 import 并注册蓝图
    """
    from routes.auth import main as routes_auth
    app.register_blueprint(routes_auth)

    from routes.test import main as routes_test
    app.register_blueprint(routes_test)

    from routes.api import main as routes_api
    app.register_blueprint(routes_api, url_prefix='/api')

    from routes.user import main as routes_user
    app.register_blueprint(routes_user, url_prefix='/user')

    from routes.blog import main as routes_blog
    app.register_blueprint(routes_blog, url_prefix='/blog')


def configure_env_vars(app):
    app.jinja_env.filters['format_time'] = format_time
    app.jinja_env.filters['from_now'] = from_now
    app.jinja_env.filters['short_time'] = short_time
    app.jinja_env.globals['csrf_token'] = gen_csrf_token
    app.jinja_env.filters['abstract'] = text_abstract


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
    else:
        user = None
    g.user = user


@app.before_request
def csrf_protect():
    white_path_list = ['/api/upload/image', '/api/upload/file']
    if request.method == 'POST':
        csrf_token = session.get('_csrf_token', '')
        if request.headers.get('content-type') == 'application/json':
            token = request.json.get('csrf_token')
        else:
            token = request.form.get('csrf_token')
        log(csrf_token, token, request.path, request.headers.get('content-type'))
        if request.path not in white_path_list:
            if not csrf_token or (csrf_token != token):
                abort(403)


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    """
    用原始的方法启动程序
    """
    app = configured_app()
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=3000,
    )
    app.run(**config)


def main():
    configured_app()
    configure_manager()
    manager.run()


if __name__ == '__main__':
    main()
