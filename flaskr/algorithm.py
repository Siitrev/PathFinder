import igraph, math


def dijkstra(G: igraph.Graph, start_v: int):
    dist = [math.inf] * len(G.vs)  # Ustawienie odleglosci na nieskonczonosc
    prev = [None] * len(G.vs)  # Ustawianie poprzednich wierzcholkow
    dist[start_v] = 0  # Odleglosc pierwszego wierzcholka
    Q = {x.index: y for (x, y) in zip(G.vs, dist)}
    directed = G.is_directed()
    while Q:
        # Wybor najmniejszej odleglosci
        min_val = min(Q.items(), key=lambda x: x[1])
        u = min_val[0]
        Q.pop(u)  # Usuniecie wierzcholka o najmniejszej odleglosci
        adjacent_vertices = G.vs[u].neighbors()  # Wybranie wszystkich sasiednich wierzcholkow

        # Przegladanie wszystkich krawedzi
        for v in adjacent_vertices:
            # Kontynuuowanie pętli jeśli wiezchołka nie ma w Q
            if v.index not in Q:
                continue
            
            edge = G.get_eid(u, v, directed=directed, error=False)  # Wyszukanie id krawedzi
            
            # Kontynuuowanie petli jesli nie ma takiej krawędzi
            if edge == -1:
                continue
            
            # Sprawdzanie czy jest to krawedz wielokrotna i wybranie najmniejszej
            if G.es[edge].is_multiple():
                start = G.es[edge].source
                end = G.es[edge].target
                edges = G.es.select(lambda e: e.source == start and e.target == end)
                alt = dist[u] + min(edges["weight"])
            else:
                alt = dist[u] + G.es[edge]["weight"]

            # Akualizowanie poszczegolnych odleglosci
            if dist[v.index] > alt:
                dist[v.index] = alt
                prev[v.index] = u

        # Aktualizacja odleglosci pozostalych wierzcholkow
        for v, d in enumerate(dist):
            if v in Q:
                Q.update({v: d})

    return dist, prev


def draw_path(G: igraph.Graph, start: int, end: int, prev: list):
    cur_v = end # Wybranie aktualnego wierzchołka
    edges = [] # Inicjalizacja tablicy krawędzi
    directed = G.is_directed() # Sprawdzenie czy graf jest skierowany
    
    # Rysowanie ścieżki od danego wierzchołka do jego celu
    while cur_v != start and prev[cur_v] != None:
        
        # Wyszukiwanie krawędzi w zależności od tego czy graf jest skierowany
        if directed:
            edge = G.es.select(lambda x: x.source == prev[cur_v] and x.target == cur_v)
        else:
            edge = G.es.select(_between=([prev[cur_v], cur_v], [prev[cur_v], cur_v]))
        
        # Dodanie krawędzi do listy krawędzi
        if len(edge):
            edge = min(edge, key=lambda e: e["weight"])
            edges.append(edge)
        cur_v = prev[cur_v]
        
    # Jeśli wierzchołek aktualny jest równy początkowemu oznacza to że znaleziono scieżke
    if cur_v == start:
        for e in edges:
            e["dijkstra_path"] = True
        return True
    return False
