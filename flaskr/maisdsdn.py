import igraph, os, time, sys
import matplotlib.pyplot as plt
from flaskr.algorithm import dijkstra, draw_path
from flaskr.util import create_graph, show_all_paths, CLEAR

if __name__ == "__main__":
    
    print(f"Ilość wierzchołków grafu {len(G.vs)}.")       
    print("Od jakiego punktu zacząć szukanie ścieżki?")
    start_v = int(input())

    if start_v not in G.vs["name"]:
        print("Nie ma takiego wierzchołka!")
        exit(1)

    print("Do jakiego wierzchołka ma iść ścieżka?")
    end_v = int(input())

    if end_v not in G.vs["name"]:
        print("Nie ma takiego wierzchołka!")
        exit(1)


    data = dijkstra(G, start_v) # Wykonanie algorytmu dijkstry
    is_path = draw_path(G, start_v, end_v, data[1])

    one_path, ax = plt.subplots(figsize=(8, 8))
    one_path.suptitle(f"Ścieżka z wierzchołka {start_v} do wierzchołka {end_v}.")
    igraph.plot(
        G,
        target=ax,
        vertex_label=G.vs["name"],
        vertex_size=0.4,
        edge_label=G.es["weight"],
        edge_color=["red" if e["dijkstra_path"] else "grey" for e in G.es],
    )
    one_path.savefig("./graf/graf_ze_ścieżką.png")
    if is_path:
        print("Znaleziono ścieżkę!")
        print(f"Odległość z wierzchołka {start_v} do {end_v} wynosi {data[0][end_v]}")
    else:
        print("Nie istnieje taka ścieżka")

    plt.show()
    os.system(CLEAR)

    print(
        """Zaprezentowac wszystkie sciezki?
        1 - Tak
        0 - Nie"""
    )

    show_all = bool(int(input()))
    if show_all:
        multiple_path, ax = plt.subplots(figsize=(8, 8))
        multiple_path.suptitle(f"Wszystkie ścieżki z wierzchołka {start_v}.")
        show_all_paths(G, data[0], start_v, data[1])
        igraph.plot(
            G,
            target=ax,
            vertex_label=G.vs["name"],
            vertex_size=0.4,
            edge_label=G.es["weight"],
            edge_color=["red" if e["dijkstra_path"] else "grey" for e in G.es],
        )
        multiple_path.savefig("./graf/graf_ze_wszystkimi_sciezkami.png")
        plt.show()

    os.system(CLEAR)
    print("Koniec dzalania programu!")
    input("Wcisnij Enter aby zakonczyc...")
    
    