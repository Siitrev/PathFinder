import igraph, datetime, os, shutil
import matplotlib
import matplotlib.pyplot as plt
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    make_response,
    send_from_directory,
    current_app,
)
from PathFinder.util import create_graph, allowed_file, show_all_paths, draw_path
from PathFinder.algorithm import dijkstra
from werkzeug.utils import secure_filename

# configure matplotlib
matplotlib.use("Agg")

# define a blueprint
bp = Blueprint("graph", __name__, url_prefix="/graph")

# route to a page for graph creation
@bp.route("/set_weights", methods=("GET", "POST"))
def set_weights():
    # create name of the graph
    name = "graph_" + datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    
    # check request method
    if request.method == "POST":
        # take data from form
        vertices = request.form["vertices"]
        directed = request.form.get("is_directed")
        if directed is None:
            directed = "0"
        else:
            directed = "1"

        # create response that renders website responsible for graph creation
        resp = make_response(
            render_template("graph_creation.html", v=int(vertices) - 1, graph_name=name)
        )
        
        # set cookies with data about graph 
        resp.set_cookie("vertices", vertices, samesite="None", secure=True, path="/")
        resp.set_cookie("directed", directed, samesite="None", secure=True, path="/")

        return resp
    # read amount of vertices of a loaded graph
    vertices = int(request.cookies.get("vertices"))
    
    # render website responsible for graph creation
    return render_template("graph_creation.html", v=vertices - 1, graph_name=name)

# route to an image 
@bp.route("/files/<name>/<filename>")
def get_image(name, filename):
    return send_from_directory(f"files/{name}", filename, as_attachment=True)

# route to a zip download
@bp.route("/download/<filename>")
def get_zip(filename):
    return send_from_directory(f"download", f"{filename}.zip", as_attachment=True)

# route to a page that shows a graph
@bp.route("/show/<name>")
def show(name: str):
    file_url = None
    if name != "None":
        file_url = url_for("graph.get_image", name=name, filename=name + ".png")
    return render_template("graph_show.html", graph_img=file_url, graph_name=name)

# route that creates the graph
@bp.route("/create/<name>", methods=("GET", "POST"))
def create(name):
    # check request method
    if request.method == "POST":
        
        # read data about edges
        tmp_edges = request.cookies.get("edges", None)
        edges = None
        
        # refactor the data
        if tmp_edges:
            tmp_edges = tmp_edges[:-1]
            tmp_edges += "]"
            edges = eval(tmp_edges)
        
        # read data about the graph
        vertices = int(request.cookies.get("vertices", None))
        directed = bool(int(request.cookies.get("directed", None)))

        # check whether there are any edges
        if edges is None:
            flash("The graph must have edges")
            return redirect(url_for("graph.set_weights"))
        else:
             
            # check if paths to upload and download folder exist
            if not os.path.exists(f"{current_app.config['UPLOAD_FOLDER']}"):
                os.mkdir(f"{current_app.config['UPLOAD_FOLDER']}")
        
            if not os.path.exists("./PathFinder/download/"):
                os.mkdir("./PathFinder/download/")
        
            if not os.path.exists(f"{current_app.config['UPLOAD_FOLDER']}{name}"):
                os.mkdir(f"{current_app.config['UPLOAD_FOLDER']}{name}")

            # create graph
            G: igraph.Graph = create_graph(n=vertices, edges=edges, directed=directed)

            # save created graph
            G.write_pickle(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}.pickle"
            )

            # create visualization of a graph
            fig, ax = plt.subplots(num=1, clear=True)
            if vertices == 1:
                fig.suptitle(f"Graph with {vertices} vertex.")
            else:
                fig.suptitle(f"Graph with {vertices} vertices.")
            igraph.plot(
                G,
                target=ax,
                vertex_label=G.vs["name"],
                edge_label=G.es["weight"],
                edge_color=["lightgrey"] * len(G.es),
                layout="circle",
            )
            
            # save graph visualization as png and pdf  
            fig.savefig(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}.png",
                transparent=True,
            )
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}.pdf")

            fig.clear()

            # read data for path draw
            start_v = int(request.form["path_start"])
            end_v = int(request.form["path_end"])

            # calculate the path using dijkstra algorithm
            dist, prev = dijkstra(G, start_v=start_v)

            # draw a path
            draw_path(G, start_v, end_v, prev)

            # create visualization of a graph with a path marked
            fig, ax = plt.subplots(num=1, clear=True)
            fig.suptitle(f"Shortest path from {start_v} to {end_v} is {dist[end_v]}")
            igraph.plot(
                G,
                target=ax,
                vertex_label=G.vs["name"],
                edge_label=G.es["weight"],
                edge_color=["red" if e["dijkstra_path"] else "lightgrey" for e in G.es],
                layout="circle",
            )
            
            # create visualization of a graph with a path, as png and pdf
            fig.savefig(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_one.png",
                transparent=True,
            )
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_one.pdf")

            fig.clear()

            # draw all paths from a given vertice
            show_all_paths(G, dist, start_v, prev)

            # create visualization of a graph with a all paths marked
            fig, ax = plt.subplots(num=1, clear=True)
            fig.suptitle(f"Shortest paths from {start_v} to all vertices")
            igraph.plot(
                G,
                target=ax,
                vertex_label=G.vs["name"],
                edge_label=G.es["weight"],
                edge_color=["red" if e["dijkstra_path"] else "lightgrey" for e in G.es],
                layout="circle",
            )
            # create visualization of a graph with a all paths, as png and pdf
            fig.savefig(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_all.png",
                transparent=True,
            )
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_all.pdf")

            fig.clear()

            # check if zip file of created graph exists
            if not os.path.exists(f"./PathFinder/download/{name}.zip"):
                # create zip file
                shutil.make_archive(
                    f"./PathFinder/download/{name}",
                    "zip",
                    f"{current_app.config['UPLOAD_FOLDER']}/{name}",
                )

            # redirect to a route that shows a graph
            return redirect(url_for("graph.show",name=name))

# route that loads a graph from a pickle file
@bp.route("/load", methods=("GET", "POST"))
def load():
    # check request method
    if request.method == "POST":
        # check if file is attached
        if "upload_file" not in request.files:
            flash("There is no file attached")
            return redirect(url_for("index"))
        
        file = request.files["upload_file"]

        # check if file is attached
        if file.filename == "":
            flash("There is no file attached")
            return redirect(url_for("index"))

        # check if extension of a file is correct
        if file and allowed_file(file.filename):
            # initialize an empty graph
            G: igraph.Graph = None

            # load a graph from a file
            G = igraph.Graph.Read_Pickle(file)

            # check whether graph is weighted
            if not G.is_weighted():
                flash("Graph isn't weighted")
                return redirect(url_for("index"))

            # check if vertices are named
            if not G.is_named():
                G.vs["name"] = list(range(len(G.vs)))

            directed = "0"
            # check if graph is directed 
            if G.is_directed():
                directed = "1"

            # create list of edges of a given graph, then refactor it to an appropriate style for a cookie
            edges = str([[e.source, e.target, int(e["weight"])] for e in G.es])
            edges = edges[:-1]
            edges = edges.replace(",", " ")

            # create response that redirects to route that allows to modificate a graph
            resp = make_response(redirect(url_for("graph.set_weights")))
            
            # set cookies with data about a graph
            resp.set_cookie(
                "vertices", str(len(G.vs)), samesite="None", secure=True, path="/"
            )
            resp.set_cookie(
                "directed", directed, samesite="None", secure=True, path="/"
            )
            resp.set_cookie("edges", edges, samesite="None", secure=True, path="/graph")

            return resp

        flash("Extension of a file is wrong (should be .pickle or .pkl)")
        return redirect(url_for("index"))

