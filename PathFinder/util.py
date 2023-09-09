import igraph

# set allowed extensions
ALLOWED_EXTENSIONS = {"pkl", "pickle"}

# function that creates a graph
def create_graph(n : int, edges : list, directed : bool = False):
    # prepare list of weights and edges
    weights = [int(w[2]) for w in edges]
    new_edges = [e[:2] for e in edges]
    
    # create a graph 
    G = igraph.Graph(n=n, edges=new_edges, directed=directed)

    # set name, weight and dijkstra_path attributes
    G.vs["name"] = [v.index for v in G.vs]
    G.es["weight"] = weights
    G.es["dijkstra_path"] = [False] * len(G.es)

    return G

# function that draws a path of a given graph from a certain vertex
def draw_path(G: igraph.Graph, start: int, end: int, prev: list):
    cur_v = end # Select current vertex
    edges = [] # Initialize edges list
    directed = G.is_directed()
    
    # Draw a path from a start to an end
    while cur_v != start and prev[cur_v] != None:
        
        # Select an edge
        if directed:
            edge = G.es.select(lambda x: x.source == prev[cur_v] and x.target == cur_v)
        else:
            edge = G.es.select(_between=([prev[cur_v], cur_v], [prev[cur_v], cur_v]))
        
        # Add an edge to an edges list
        if len(edge):
            edge = min(edge, key=lambda e: e["weight"])
            edges.append(edge)
        cur_v = prev[cur_v]
        
    # If currently processed vertex is equal to a starting vertex, the path is found.
    if cur_v == start:
        for e in edges:
            e["dijkstra_path"] = True
        return True
    return False

# function that draws all paths of a given graph from a certain vertex
def show_all_paths(G: igraph.Graph, dist: list, start_v: int, prev: list):
    # use draw_path function on all of the vertices of the graph, except the one that is a starting point
    for i in range(len(dist)):
        if i == start_v:
            continue
        draw_path(G, start_v, i, prev)

# function that checks the extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS