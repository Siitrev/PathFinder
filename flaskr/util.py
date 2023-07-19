import igraph, os, asyncio
from flaskr.algorithm import draw_path

ALLOWED_EXTENSIONS = {"pkl", "pickle", "graphmlz"}

# Funkcja odpowiedzialna za tworzenie garfu
def create_graph(n : int, edges : list, directed : bool = False):
    weights = [w[2] for w in edges]
    new_edges = [e[:2] for e in edges]
    G = igraph.Graph(n=n, edges=new_edges, directed=directed)

    G.vs["name"] = [v.index for v in G.vs]
    G.es["weight"] = weights
    G.es["dijkstra_path"] = [False] * len(G.es)

    return G


def show_all_paths(G: igraph.Graph, dist: list, start_v: int, prev: list):
    # Przejrzenie wszystkich wierzchołków i uruchomienie dla nich funkcji rysującej ścieżkę
    for i in range(len(dist)):
        if i == start_v:
            continue
        if draw_path(G, start_v, i, prev):
            print(f"Odleglość z punktu {start_v} do punktu {i} wynosi {dist[i]}.")
        else:
            print(f"Nie ma ścieżki z punktu {start_v} do punktu {i}.")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS