from flask import Blueprint

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')  # http://127.0.0.1:5000
def index():
    pass
