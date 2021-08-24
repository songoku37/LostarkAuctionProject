from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def redirectStatus():
    return redirect(url_for('status.status'))