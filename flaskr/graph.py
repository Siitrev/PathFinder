import igraph, datetime, json
import matplotlib
import matplotlib.pyplot as plt
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, make_response, send_from_directory, current_app
)
from flaskr.util import create_graph, allowed_file
from flaskr.algorithm import dijkstra
from werkzeug.utils import secure_filename

matplotlib.use('Agg')
bp = Blueprint('graph', __name__, url_prefix='/graph')



@bp.route('/set_weights', methods=('GET', 'POST'))
def set_weights():
    name = "graph_" + datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    if request.method == "POST":
        vertices = request.form["vertices"]
        directed = request.form.get("is_directed")
        if directed is None:
            directed = "0"
        else:
            directed = "1"
        
        resp = make_response( render_template('graph_creation.html', v = int(vertices)-1, graph_name = name))
        resp.set_cookie("vertices", vertices, samesite="None", secure=True, path="/")
        resp.set_cookie("directed", directed, samesite="None", secure=True, path="/")
            
        return resp
    vertices = int(request.cookies.get("vertices"))
    return render_template('graph_creation.html', v = vertices-1, graph_name = name)

@bp.route('/files/<filename>')
def get_image(filename):
    return send_from_directory("files", filename, as_attachment=True)

@bp.route('/show/<name>')
def show(name):
    file_url = None
    if name != "None":
        file_url = url_for('graph.get_image', filename=name + ".png")
    return render_template('graph_show.html', graph_img = file_url)

@bp.route('/show_saved', methods=('GET', 'POST'))
def show_saved():
    if request.method == "POST":
        if "upload_file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["upload_file"]
        
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            
            G : igraph.Graph = None
            
            filename = secure_filename(file.filename)
            
            name, ext = filename.rsplit('.', 1)
            
            if ext == "pkl" or ext == "pickle":
                G = igraph.Graph.Read_Pickle(file)
            elif ext == "graphmlz":
                G = igraph.Graph.Read_GraphMLz(file)
            
            if not G.is_weighted():
                flash("Graph isn't weighted")
                return redirect(request.url)
            
            if not G.is_named():
                G.vs["name"] = list(range(len(G.vs)))
            
        
            return render_template("graph_show_saved.html", graph=G)
        
        flash("Wrong file ext")
    return render_template("graph_show_saved.html")
    
@bp.route('/create/<name>', methods=('GET', 'POST'))            
def create(name):
    if request.method == "POST":
        tmp_edges = request.cookies.get("edges", None)[:-1]
        edges = None
        if tmp_edges:
            tmp_edges += "]"
            edges = eval(tmp_edges)
        vertices = int(request.cookies.get("vertices", None))  
        directed = bool(int(request.cookies.get("directed", None)))      
        
        if edges is None:
            flash("No edges")
            return redirect(url_for("graph.show",name="None"))
        else:
            G : igraph.Graph = create_graph(n=vertices, edges=edges, directed=directed)
            fig, ax = plt.subplots(num=1,clear=True)
            igraph.plot(G,
                            target=ax,
                            vertex_label=G.vs["name"],
                            edge_label=G.es["weight"],
                            edge_color=["lightgrey"] * len(G.es),
                            layout="circle")
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}{name}.png", transparent=True)
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}{name}.pdf")
            
            start_v = int(request.cookies.get("start_v"))
            
            dist, prev = dijkstra(G, start_v)
            
            fig, ax = plt.subplots(num=1,clear=True)
            
            answer = {"dist": dist, "prev":prev}
            
            resp = make_response(json.dumps(answer),200)
            
            return resp
    
@bp.route('/load', methods=('GET', 'POST'))
def load():
    if request.method == "POST":
        if "upload_file" not in request.files:
            flash("No file part")
            return redirect(url_for("graph.show", name="None"))
        
        file = request.files["upload_file"]
        
        if file.filename == "":
            flash("No selected file")
            return redirect(url_for("graph.show", name="None"))
        
        if file and allowed_file(file.filename):
            
            G : igraph.Graph = None
            
            filename = secure_filename(file.filename)
            
            _ , ext = filename.rsplit('.', 1)
            
            if ext == "pkl" or ext == "pickle":
                G = igraph.Graph.Read_Pickle(file)
            elif ext == "graphmlz":
                G = igraph.Graph.Read_GraphMLz(file)
            
            if not G.is_weighted():
                flash("Graph isn't weighted")
                return redirect(url_for("graph.show", name="None"))
            
            if not G.is_named():
                G.vs["name"] = list(range(len(G.vs)))
                
            directed = "0"
            if G.is_directed():
                directed = "1"
                            
                            
            edges = str([[e.source, e.target, int(e["weight"])] for e in G.es])
            edges = edges[:-1]
            edges = edges.replace(","," ")
            
            resp = make_response( redirect(url_for("graph.set_weights")))
            resp.set_cookie("vertices", str(len(G.vs)), samesite="None", secure=True, path="/")
            resp.set_cookie("directed", directed, samesite="None", secure=True, path="/")
            resp.set_cookie("edges", edges, samesite="None", secure=True, path="/graph")
            
            return resp
        
        flash("Wrong file ext")
        return redirect(url_for("graph.show", name="None"))
      

    
    
    
