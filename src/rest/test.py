from flask import Blueprint

bp = Blueprint('test', __name__)

@bp.route('/')
def hello_world():
    return 'Hello World!'

