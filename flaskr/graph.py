import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/set_weights', methods=('GET', 'POST'))
def set_weights():
    if request.method == "POST":    
        if not session.get("edges",None) is None:
            session["edges"] = "["
        if not session.get("vertices",None):
            session["vertices"] = request.form["vertices"]
        return render_template('graph_creation.html')

@bp.route('/show', methods=('GET', 'POST'))
def show_graph():
    for key in list(session.keys()):
        session.pop(key)
    session["edges"] = "["
    session["verices"] = 0
    return render_template('graph_show.html')
