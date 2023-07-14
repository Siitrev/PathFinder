import igraph
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, make_response
)
from flaskr.util import create_graph

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/set_weights', methods=('GET', 'POST'))
def set_weights():
    if request.method == "POST":
        vertices = request.form["vertices"]
        directed = request.form.get("is_directed")
        if directed is None:
            directed = "0"
        else:
            directed = "1"
        resp = make_response( render_template('graph_creation.html', v = int(vertices)-1))
        resp.set_cookie("vertices", vertices, samesite=None, secure=True)
        resp.set_cookie("directed", directed, samesite=None, secure=True)
            
        return resp

@bp.route('/show', methods=('GET', 'POST'))
def show_graph():
    code = 400
    if request.method == "POST":
        tmp_edges = request.cookies.get("edges", None)[:-1] + "]"
        vertices = int(request.cookies.get("vertices", None))  
        directed = bool(int(request.cookies.get("directed", None)))      
        edges = eval(tmp_edges)
        if not edges:
            code = 501
        else:
            G : igraph.Graph = create_graph(n=vertices, edges=edges, directed=directed)
            igraph.plot(G, target='myfile.pdf',
                        vertex_label=G.vs["name"],
                        edge_label=G.es["weight"],
                        edge_color=["lightgrey"] * len(G.es))
            return render_template('graph_show.html', code=code, vertic = G.vs)
            
    return render_template('graph_show.html', code=code)
            
        

    
    
    
