import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, make_response
)

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/set_weights', methods=('GET', 'POST'))
def set_weights():
    if request.method == "POST":
           
        resp = make_response( render_template('graph_creation.html'))
        vertices = request.form["vertices"]
        resp.set_cookie("vertices", vertices,samesite=None, secure=True)
            
        return resp

@bp.route('/show', methods=('GET', 'POST'))
def show_graph():
    code = 400
    if request == "POST":
        tmp_edges = request.cookies.get("edges",None)[:-1] + "]"
        edges = eval(tmp_edges)
        if not edges:
            code = 501
            
    return render_template('graph_show.html', code=code)
    
    
    
