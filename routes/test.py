from flask import Blueprint
from flask import Markup
from flask import render_template

from utils import log

main = Blueprint('test', __name__)


@main.route('/test')
def test():
    return render_template('test.html')
