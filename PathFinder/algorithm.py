import igraph, math


def dijkstra(G: igraph.Graph, start_v: int):
    dist = [math.inf] * len(G.vs)  # Initialize distances 
    prev = [None] * len(G.vs)  # initialize predecessors
    dist[start_v] = 0  # Set distance to first vertex
    
    Q = {x.index: y for (x, y) in zip(G.vs, dist)}
    directed = G.is_directed()
    while Q:
        # Select lowest distance
        min_val = min(Q.items(), key=lambda x: x[1])
        u = min_val[0]
        Q.pop(u)  # Remove vertex with lowest distance from dictionary
        adjacent_vertices = G.vs[u].neighbors()  # Select all of the neighbours

        # Go through all edges
        for v in adjacent_vertices:
            # If vertex is in Q dictionary continue the algorithm
            if v.index not in Q:
                continue
            
            edge = G.get_eid(u, v, directed=directed, error=False)  # Search for an edge with given id
            
            # Skip the rest of the code if that edge doesn't exist
            if edge == -1:
                continue
            
            # Check whether the edge is multiple and if it is multiple, select the one with smaller weight
            if G.es[edge].is_multiple():
                start = G.es[edge].source
                end = G.es[edge].target
                edges = G.es.select(lambda e: e.source == start and e.target == end)
                alt = dist[u] + min(edges["weight"])
            else:
                alt = dist[u] + G.es[edge]["weight"]

            # Update the distance of vertices
            if dist[v.index] > alt:
                dist[v.index] = alt
                prev[v.index] = u

        # Update the distances of the rest of vertices
        for v, d in enumerate(dist):
            if v in Q:
                Q.update({v: d})

    return dist, prev

