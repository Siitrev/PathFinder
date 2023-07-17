import igraph, datetime
import matplotlib.pyplot as plt
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, make_response, send_from_directory, current_app
)
from flaskr.util import create_graph
from werkzeug.utils import secure_filename


bp = Blueprint('graph', __name__, url_prefix='/graph')

ALLOWED_EXTENSIONS = {"pkl", "pickle", "graphmlz"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/set_weights', methods=('GET', 'POST'))
def set_weights():
    if request.method == "POST":
        vertices = request.form["vertices"]
        directed = request.form.get("is_directed")
        if directed is None:
            directed = "0"
        else:
            directed = "1"
        name = "graph_" + datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        resp = make_response( render_template('graph_creation.html', v = int(vertices)-1, graph_name = name))
        resp.set_cookie("vertices", vertices, samesite=None, secure=True)
        resp.set_cookie("directed", directed, samesite=None, secure=True)
            
        return resp

@bp.route('/files/<filename>')
def get_image(filename):
    return send_from_directory("files", filename, as_attachment=True)

@bp.route('/show/<name>')
def show(name):
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
            
            
            # if graph is not None:
            #     fig, ax = plt.subplots()
            #     igraph.plot(graph,
            #                 target=ax,
            #                 vertex_label=graph.vs["name"],
            #                 edge_label=graph.es["weight"],
            #                 edge_color=["lightgrey"] * len(graph.es),
            #                 layout="circle")
            #     fig.savefig("myfile2.pdf")
        
            return render_template("graph_show_saved.html", graph=G)
        
        flash("Wrong file ext")
    return render_template("graph_show_saved.html")
    
@bp.route('/creating/<name>', methods=('GET', 'POST'))            
def creating(name):
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
            return redirect(request.url)
        else:
            G : igraph.Graph = create_graph(n=vertices, edges=edges, directed=directed)
            igraph.plot(G,
                        target=f"{current_app.config['UPLOAD_FOLDER']}{name}.png",
                        vertex_label=G.vs["name"],
                        edge_label=G.es["weight"],
                        edge_color=["lightgrey"] * len(G.es),
                        layout="circle")
            return render_template("loading.html")
    
            

    
    
    
