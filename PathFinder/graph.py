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
from PathFinder.util import create_graph, allowed_file, show_all_paths
from PathFinder.algorithm import dijkstra, draw_path
from werkzeug.utils import secure_filename

matplotlib.use("Agg")
bp = Blueprint("graph", __name__, url_prefix="/graph")


@bp.route("/set_weights", methods=("GET", "POST"))
def set_weights():
    name = "graph_" + datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    if request.method == "POST":
        vertices = request.form["vertices"]
        directed = request.form.get("is_directed")
        if directed is None:
            directed = "0"
        else:
            directed = "1"

        resp = make_response(
            render_template("graph_creation.html", v=int(vertices) - 1, graph_name=name)
        )
        resp.set_cookie("vertices", vertices, samesite="None", secure=True, path="/")
        resp.set_cookie("directed", directed, samesite="None", secure=True, path="/")

        return resp
    vertices = int(request.cookies.get("vertices"))
    return render_template("graph_creation.html", v=vertices - 1, graph_name=name)


@bp.route("/files/<name>/<filename>")
def get_image(name, filename):
    return send_from_directory(f"files/{name}", filename, as_attachment=True)


@bp.route("/download/<filename>")
def get_zip(filename):
    return send_from_directory(f"download", f"{filename}.zip", as_attachment=True)


@bp.route("/show/<name>")
def show(name: str):
    file_url = None
    if name != "None":
        file_url = url_for("graph.get_image", name=name, filename=name + ".png")
    return render_template("graph_show.html", graph_img=file_url, graph_name=name)


@bp.route("/create/<name>", methods=("GET", "POST"))
def create(name):
    if request.method == "POST":
        tmp_edges = request.cookies.get("edges", None)
        edges = None
        if tmp_edges:
            tmp_edges = tmp_edges[:-1]
            tmp_edges += "]"
            edges = eval(tmp_edges)
        vertices = int(request.cookies.get("vertices", None))
        directed = bool(int(request.cookies.get("directed", None)))

        if edges is None:
            flash("The graph must have edges")
            return redirect(url_for("graph.set_weights"))
        else:
            if not os.path.exists(f"{current_app.config['UPLOAD_FOLDER']}{name}"):
                os.mkdir(f"{current_app.config['UPLOAD_FOLDER']}{name}")

            G: igraph.Graph = create_graph(n=vertices, edges=edges, directed=directed)

            G.write_pickle(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}.pickle"
            )

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
            fig.savefig(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}.png",
                transparent=True,
            )
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}.pdf")

            fig.clear()

            start_v = int(request.form["path_start"])
            end_v = int(request.form["path_end"])

            dist, prev = dijkstra(G, start_v=start_v)

            draw_path(G, start_v, end_v, prev)

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
            fig.savefig(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_one.png",
                transparent=True,
            )
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_one.pdf")

            fig.clear()

            show_all_paths(G, dist, start_v, prev)

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
            fig.savefig(
                f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_all.png",
                transparent=True,
            )
            fig.savefig(f"{current_app.config['UPLOAD_FOLDER']}/{name}/{name}_all.pdf")

            fig.clear()

            if not os.path.exists(f"./PathFinder/download/{name}.zip"):
                shutil.make_archive(
                    f"./PathFinder/download/{name}",
                    "zip",
                    f"{current_app.config['UPLOAD_FOLDER']}/{name}",
                )

            return redirect(url_for("graph.show",name=name))


@bp.route("/load", methods=("GET", "POST"))
def load():
    if request.method == "POST":
        if "upload_file" not in request.files:
            flash("There is no file attached")
            return redirect(url_for("index"))

        file = request.files["upload_file"]

        if file.filename == "":
            flash("There is no file attached")
            return redirect(url_for("index"))

        if file and allowed_file(file.filename):
            G: igraph.Graph = None

            filename = secure_filename(file.filename)

            _, ext = filename.rsplit(".", 1)

            G = igraph.Graph.Read_Pickle(file)

            if not G.is_weighted():
                flash("Graph isn't weighted")
                return redirect(url_for("index"))

            if not G.is_named():
                G.vs["name"] = list(range(len(G.vs)))

            directed = "0"
            if G.is_directed():
                directed = "1"

            edges = str([[e.source, e.target, int(e["weight"])] for e in G.es])
            edges = edges[:-1]
            edges = edges.replace(",", " ")

            resp = make_response(redirect(url_for("graph.set_weights")))
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

# @bp.route("/draw/single/<name>", methods=("GET", "POST"))
# def draw_one(name):
#     if request.method == "POST":
#         G: igraph.Graph = igraph.Graph.Read_Pickle(
#             f"{current_app.config['UPLOAD_FOLDER']}{name}.pickle"
#         )

#         start_v = int(request.cookies.get("start_v"))
#         end_v = int(request.cookies.get("end_v"))

#         dist, prev = dijkstra(G, start_v=start_v)

#         draw_path(G, start_v, end_v, prev)

#         fig, ax = plt.subplots(num=1, clear=True)
#         fig.suptitle(f"Shortest path from {start_v} to {end_v} is {dist[end_v]}")
#         igraph.plot(
#             G,
#             target=ax,
#             vertex_label=G.vs["name"],
#             edge_label=G.es["weight"],
#             edge_color=["red" if e["dijkstra_path"] else "lightgrey" for e in G.es],
#             layout="circle",
#         )
#         fig.savefig(
#             f"{current_app.config['UPLOAD_FOLDER']}{name}_one.png", transparent=True
#         )

#         fig.clear()

#         return make_response("OK", 302)


# @bp.route("/draw/all/<name>", methods=("GET", "POST"))
# def draw_all(name):
#     if request.method == "POST":
#         G: igraph.Graph = igraph.Graph.Read_Pickle(
#             f"{current_app.config['UPLOAD_FOLDER']}{name}.pickle"
#         )

#         start_v = int(request.cookies.get("start_v"))

#         dist, prev = dijkstra(G, start_v=start_v)

#         show_all_paths(G, dist, start_v, prev)

#         fig, ax = plt.subplots(num=1, clear=True)
#         fig.suptitle(f"Shortest paths from {start_v} to all vertices")
#         igraph.plot(
#             G,
#             target=ax,
#             vertex_label=G.vs["name"],
#             edge_label=G.es["weight"],
#             edge_color=["red" if e["dijkstra_path"] else "lightgrey" for e in G.es],
#             layout="circle",
#         )
#         fig.savefig(
#             f"{current_app.config['UPLOAD_FOLDER']}{name}_all.png", transparent=True
#         )

#         fig.clear()

#         return make_response("OK", 302)
