"""
Opsi A, menjalankan BFS dan DFS lalu mencetak tabel trace di terminal.

    uv run main.py                 # rute Rumah ke UC Makassar
    uv run main.py --graph page08  # graf validasi Page 08
"""

import argparse

from core.graphs import PAGE08, ROUTE_HOME_TO_UC
from core.search import QueueFrontier, StackFrontier, graph_search

GRAPH_CHOICES = {
    "route": {
        "graph": ROUTE_HOME_TO_UC,
        "start": "Rumah",
        "goal": "UC Makassar",
        "title": "Rute Rumah ke UC Makassar",
    },
    "page08": {
        "graph": PAGE08,
        "start": "Denpasar",
        "goal": "Padangbai",
        "title": "Graf Page 08 (validasi)",
    },
}


def print_summary(algorithm_name, path, explored_order):
    print(algorithm_name)
    if path is None:
        print("  Path            : tidak ditemukan")
    else:
        path_text = " -> ".join(path)
        number_of_steps = len(path) - 1
        print(f"  Path            : {path_text}")
        print(f"  Langkah jalur   : {number_of_steps}")
    print(f"  Node diekspansi : {len(explored_order)}")


def main():
    parser = argparse.ArgumentParser(description="GRAPH-SEARCH BFS dan DFS")
    parser.add_argument("--graph", choices=GRAPH_CHOICES.keys(), default="route")
    args = parser.parse_args()

    choice = GRAPH_CHOICES[args.graph]
    graph = choice["graph"]
    start = choice["start"]
    goal = choice["goal"]
    title = choice["title"]
    print(f"{title}  ({start} -> {goal})")

    print("\n=== BFS ===")
    bfs_path, bfs_explored_order = graph_search(
        start, goal, QueueFrontier(), graph, trace=True
    )

    print("\n=== DFS ===")
    dfs_path, dfs_explored_order = graph_search(
        start, goal, StackFrontier(), graph, trace=True
    )

    print("\n=== Ringkasan ===")
    print_summary("BFS", bfs_path, bfs_explored_order)
    print_summary("DFS", dfs_path, dfs_explored_order)


if __name__ == "__main__":
    main()
