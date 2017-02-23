from functools import wraps
import time
import os
import uuid
import inspect
from random import randint
from datetime import datetime
import hashlib
from termcolor import colored
from lxml.html.clean import Cleaner

from flask import session
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import Markup
from flask import g

from config import *


def log(*args, s=''):
    try:
        supplement = s
        frame = inspect.getframeinfo(inspect.currentframe().f_back)
        line_number = frame[1]
        for line in frame[3]:
            begin = line.find('(') + 1
            end = line.rfind(')')
            name_list = line[begin:end].split(',')
            for name, value in zip(name_list, args):
                name = name.strip()
                result = [
                    colored("debug({})".format(line_number), "blue"),
                    colored("{}".format(name), attrs=['bold']),
                    colored("--->", "white"),
                    colored('{}    {}'.format(value, type(value))),
                ]
                if supplement:
                    s = colored('[{}]'.format(s), 'blue')
                    result.insert(2, s)
                print(' '.join(result))
    except:
        print(colored("debug ", "red") + "something wrong")


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_view'))
        return f(*args, **kwargs)

    return function


def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not g.user.is_admin():
            r = {
                'success': False,
                'message': '无权操作, 需要管理员身份!',
            }
            return jsonify(r)
        return f(*args, **kwargs)

    return wrapped


def format_time(timestamp):
    t = time.localtime(timestamp)
    time_format = '%Y-%m-%d %H:%M'
    ft = time.strftime(time_format, t)
    return ft


def short_time(timestamp):
    time_format = '%m/%d %H:%M'
    t = time.localtime(timestamp)
    ft = time.strftime(time_format, t)
    return ft


def from_now(timestamp):
    now = int(time.time())
    from_now = now - timestamp
    a_minute = 60
    an_hour = 60 * 60
    a_day = 60 * 60 * 24
    a_week = 60 * 60 * 24 * 7
    a_month = 60 * 60 * 24 * 30
    a_year = 60 * 60 * 24 * 365
    if from_now < an_hour:
        from_now_int = int(from_now / a_minute)
        from_now_str = '{} 分钟前'.format(from_now_int)
    elif from_now < a_day:
        from_now_int = int(from_now / an_hour)
        from_now_str = '{} 小时前'.format(from_now_int)
    elif from_now < a_week:
        from_now_int = int(from_now / a_day)
        from_now_str = '{} 天前'.format(from_now_int)
    elif from_now < a_month:
        from_now_int = int(from_now / a_week)
        from_now_str = '{} 周前'.format(from_now_int)
    elif from_now < a_year:
        from_now_int = int(from_now / a_month)
        from_now_str = '{} 月前'.format(from_now_int)
    else:
        from_now_int = int(from_now / a_year)
        from_now_str = '{} 年前'.format(from_now_int)
    return from_now_str


def gen_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid.uuid4())
    return session['_csrf_token']


def sanitize(text):
    if text.strip():
        cleaner = Cleaner(safe_attrs_only=False, style=True)
        return cleaner.clean_html(text)
    else:
        return text


def text_abstract(text):
    return Markup(text).striptags()[0:100]


def rand_str():
    random_num = randint(100000, 999999)
    raw_str = str(datetime.utcnow()) + str(random_num)
    hash_fac = hashlib.new('ripemd160')
    hash_fac.update(raw_str.encode('utf-8'))
    return hash_fac.hexdigest()


def allowed_file(filename, type):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS[type]


def handle_upload(file, type):
    r = {
        'success': False,
    }
    if file and allowed_file(file.filename, type):
        old_filename = file.filename
        file_suffix = old_filename.split('.')[-1]
        new_filename = rand_str() + '.' + file_suffix
        try:
            upload_path = os.path.join(UPLOAD_FOLDER, type + 's/')
            file.save(os.path.join(upload_path, new_filename))
        except FileNotFoundError:
            os.makedirs(upload_path)
            file.save(os.path.join(upload_path, new_filename))
        except Exception as e:
            r['message'] = e
            return r
        r['success'] = True
        r['old_filename'] = old_filename
        r['new_filename'] = new_filename
        return r
    r['message'] = "不支持该文件格式"
    return r
