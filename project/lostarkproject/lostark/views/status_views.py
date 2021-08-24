from flask import Blueprint, render_template

bp = Blueprint('status',__name__, url_prefix='/status')

@bp.route('/')
def status():
    return render_template('status/status.html')
