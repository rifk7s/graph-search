"""
Opsi B, menggambar graf rute Rumah ke UC Makassar ke file PNG.
Jalur dicari dengan graph_search dari search.py (bukan fungsi networkx).

    uv run python -m core.visualize
"""

import os

import matplotlib

# Backend Agg harus dipilih sebelum pyplot di-import, supaya gambar
# langsung disimpan ke file tanpa membuka jendela
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

from core.graphs import ROUTE_HOME_TO_UC
from core.search import QueueFrontier, StackFrontier, graph_search

START = "Rumah"
GOAL = "UC Makassar"
OUTPUT_DIR = "output"

# Posisi manual meniru peta, Rumah di kanan atas dan UC Makassar di kiri bawah.
# Rute A di kolom kiri, rute B di tengah, rute C di kanan, supaya tidak ada garis bersilangan.
NODE_POSITIONS = {
    "Rumah": (10, 15.5),
    "Jl. Tarakan": (8, 14.5),
    # Rute A
    "Jl. Nusantara": (5.5, 13),
    "Jl. Riburane": (4, 11.5),
    "Jl. Ahmad Yani": (3, 10),
    "Jl. Kajaolalido": (3, 8.5),
    "Jl. Botolempangan": (3.5, 6.5),
    # Rute B
    "Jl. Yos Sudarso": (8, 12.5),
    "Jl. Andalas": (7.5, 11),
    "Jl. Gunung Latimojong": (7, 9.5),
    "Jl. G. Bawakaraeng": (7, 8),
    "Jl. Jend. Sudirman": (7, 6.5),
    "Jl. Ince Nurdin": (5.25, 5.75),
    # Rute C
    "Jl. Tentara Pelajar": (12, 13.5),
    "Jl. Sarappo": (12.5, 11),
    "Jl. Ternate": (12.5, 9.5),
    "Jl. Lembeh": (12.5, 8),
    "Jl. KH Wahid Hasyim": (12, 6.5),
    "Jl. HOS Cokroaminoto": (9.75, 6.5),
    # Bagian yang sama untuk ketiga rute
    "Jl. Arief Rate": (3, 5),
    "Jl. H. Bau": (3, 3.5),
    "Jl. Metro Tj. Bunga": (2.5, 2),
    "UC Makassar": (1, 0.5),
}

COLOR_PATH = "#eb6834"  # oranye
COLOR_EXPLORED_NOT_PATH = "#2a78d6"  # biru
COLOR_NOT_EXPLORED = "#c3c2b7"  # abu-abu
COLOR_TEXT = "#0b0b0b"

FIGURE_SIZE_INCHES = (13, 14)
PATH_EDGE_WIDTH = 4
NORMAL_EDGE_WIDTH = 1.5
LABEL_OFFSET_ABOVE_NODE = 0.45


def build_networkx_graph():
    route_graph = nx.Graph()
    for street, neighbors in ROUTE_HOME_TO_UC.items():
        for neighbor in neighbors:
            # Tiap edge muncul dua kali di dict adjacency,
            # networkx mengabaikan edge yang sudah ada
            route_graph.add_edge(street, neighbor)
    return route_graph


def get_path_edges(path):
    path_edges = set()
    for index in range(len(path) - 1):
        current_street = path[index]
        next_street = path[index + 1]
        # Graf tidak berarah, edge bisa tercatat dari arah mana saja
        path_edges.add((current_street, next_street))
        path_edges.add((next_street, current_street))
    return path_edges


def draw_route_png(algorithm_name, path, explored_order, file_name):
    route_graph = build_networkx_graph()
    path_edges = get_path_edges(path)

    node_list = list(route_graph.nodes)
    node_colors = []
    for street in node_list:
        if street in path:
            node_colors.append(COLOR_PATH)
        elif street in explored_order:
            node_colors.append(COLOR_EXPLORED_NOT_PATH)
        else:
            node_colors.append(COLOR_NOT_EXPLORED)

    edge_list = list(route_graph.edges)
    edge_colors = []
    edge_widths = []
    for edge in edge_list:
        if edge in path_edges:
            edge_colors.append(COLOR_PATH)
            edge_widths.append(PATH_EDGE_WIDTH)
        else:
            edge_colors.append(COLOR_NOT_EXPLORED)
            edge_widths.append(NORMAL_EDGE_WIDTH)

    figure, axes = plt.subplots(figsize=FIGURE_SIZE_INCHES)
    nx.draw_networkx_edges(
        route_graph,
        NODE_POSITIONS,
        ax=axes,
        edgelist=edge_list,
        edge_color=edge_colors,
        width=edge_widths,
    )
    nx.draw_networkx_nodes(
        route_graph,
        NODE_POSITIONS,
        ax=axes,
        nodelist=node_list,
        node_color=node_colors,
        node_size=500,
        edgecolors="white",
        linewidths=2,
    )

    # Label diberi latar putih supaya tetap terbaca walaupun dilewati garis edge
    label_positions = {}
    for street in NODE_POSITIONS:
        x, y = NODE_POSITIONS[street]
        label_positions[street] = (x, y + LABEL_OFFSET_ABOVE_NODE)
    nx.draw_networkx_labels(
        route_graph,
        label_positions,
        ax=axes,
        font_size=10,
        font_color=COLOR_TEXT,
        bbox=dict(facecolor="white", edgecolor="none", pad=1.5),
    )

    # Line2D di bawah tidak ikut digambar, hanya contoh simbol untuk legenda
    path_legend = Line2D(
        [0],
        [0],
        marker="o",
        color=COLOR_PATH,
        linewidth=4,
        markersize=12,
        label="Jalur solusi",
    )
    explored_legend = Line2D(
        [0],
        [0],
        marker="o",
        color="white",
        markerfacecolor=COLOR_EXPLORED_NOT_PATH,
        markersize=12,
        label="Diekspansi, bukan jalur",
    )
    not_explored_legend = Line2D(
        [0],
        [0],
        marker="o",
        color=COLOR_NOT_EXPLORED,
        linewidth=1.5,
        markersize=12,
        label="Tidak diekspansi",
    )
    axes.legend(
        handles=[path_legend, explored_legend, not_explored_legend],
        loc="upper left",
        frameon=False,
    )

    number_of_steps = len(path) - 1
    number_expanded = len(explored_order)
    axes.set_title(
        f"{algorithm_name} dari {START} ke {GOAL}\n"
        f"{number_of_steps} langkah jalur, {number_expanded} node diekspansi",
        color=COLOR_TEXT,
    )
    axes.margins(0.12)
    axes.axis("off")

    figure.tight_layout()
    figure.savefig(file_name, dpi=150)
    plt.close(figure)

    path_text = " -> ".join(path)
    print(f"{algorithm_name}: {path_text}")
    print(f"     disimpan ke {file_name}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    bfs_path, bfs_explored_order = graph_search(
        START, GOAL, QueueFrontier(), ROUTE_HOME_TO_UC
    )
    draw_route_png(
        "BFS", bfs_path, bfs_explored_order, os.path.join(OUTPUT_DIR, "bfs_route.png")
    )

    dfs_path, dfs_explored_order = graph_search(
        START, GOAL, StackFrontier(), ROUTE_HOME_TO_UC
    )
    draw_route_png(
        "DFS", dfs_path, dfs_explored_order, os.path.join(OUTPUT_DIR, "dfs_route.png")
    )


if __name__ == "__main__":
    main()
