from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/auth/login')  # http://127.0.0.1:5000/auth/login
def login():
    pass
