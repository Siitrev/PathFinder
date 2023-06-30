import igraph, os, math
from sys import platform
from algorithm import draw_path

# Sprawdzenie systemu operacyjnego
CLEAR = "cls"
if platform == "linux" or platform == "linux2":
    CLEAR = "clear"

# Funkcja odpowiedzialna za tworzenie garfu
def create_graph():
    n = int(input("Proszę podać ilość wierzchołków grafu: "))
    if n < 1:
        print("Niepoprawna ilosc wierzcholkow!")
        exit(1)
    os.system(CLEAR)
    edges = []
    weights = []
    # Dodawanie krawędzi
    while True:
        print(f"Ilosc wierzchołków w grafie {n}.")
        print("Aby zakonczyc dodawanie wierzchołków to nalezy wpisać -1 przy początkowym wierzchołku")
        edge = []
        edge.append(int(input("Proszę podać początek krawędzi: ")))
        if edge[0] == -1:
            os.system(CLEAR)
            break
        edge.append(int(input("Proszę podać koniec krawędzi: ")))
        weight = int(input("Proszę podać wagę tej krawędzi: "))
        for v in edge:
            if v < -1 or v >= n:
                print("Podano błędne wierzchołki")
                input("Naciśnij Enter żeby kontynuować...")
                continue
        if weight < 0:
            print("Podano błędną wage")
            input("Naciśnij Enter żeby kontynuować...")
            continue

        edges.append(edge)
        weights.append(weight)
        os.system(CLEAR)

    print(
        """Czy graf ma byc skierowany?
          1 - Tak
          0 - Nie"""
    )
    directed = bool(int(input()))
    os.system(CLEAR)
    G = igraph.Graph(n=n, edges=edges, directed=directed)

    G.vs["name"] = [v.index for v in G.vs]
    G.es["weight"] = weights
    G.es["dijkstra_path"] = [False] * len(G.es)

    print(
        """Utworzono graf! Zapisać go?
        1 - Tak
        0 - Nie"""
    )
    save = bool(int(input()))
    if save:
        G.write_pickle("./graf/graf.p")
    os.system(CLEAR)

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
