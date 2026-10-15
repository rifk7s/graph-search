"""
Algoritma GRAPH-SEARCH tanpa bobot (gaya CS50 AI).
File ini hanya memakai standard library.
"""


class Node:
    """Simpul pencarian, menyimpan state dan parent (node asalnya)."""

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent


class StackFrontier:
    """Frontier LIFO (tumpukan), dipakai untuk DFS."""

    # Stack mengeluarkan node yang terakhir masuk. Supaya tetangga dengan
    # abjad terkecil keluar lebih dulu, tetangga harus dimasukkan terbalik.
    add_children_in_reverse_order = True

    def __init__(self):
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def contains_state(self, state):
        for node in self.nodes:
            if node.state == state:
                return True
        return False

    def empty(self):
        return len(self.nodes) == 0

    def remove(self):
        if self.empty():
            raise Exception("frontier kosong")
        last_index = len(self.nodes) - 1
        newest_node = self.nodes.pop(last_index)
        return newest_node


# Mewarisi StackFrontier karena add, empty, dan contains_state sama persis.
# Yang berbeda hanya node mana yang dikeluarkan dan urutan memasukkan anak.
class QueueFrontier(StackFrontier):
    """Frontier FIFO (antrian), dipakai untuk BFS."""

    add_children_in_reverse_order = False

    def remove(self):
        if self.empty():
            raise Exception("frontier kosong")
        first_index = 0
        oldest_node = self.nodes.pop(first_index)
        return oldest_node


def graph_search(
    start, goal, frontier, graph, include_goal_in_explored=False, trace=False
):
    """
    Mencari jalur dari start ke goal.
    Mengembalikan (path, explored_order). path bernilai None kalau tidak ada jalur.
    """
    frontier.add(Node(start))
    explored_set = set()
    explored_order = []
    trace_rows = []
    path = None

    # Langkah 1 GRAPH-SEARCH, gagal kalau frontier kosong
    while not frontier.empty():
        # Langkah 2 GRAPH-SEARCH, keluarkan node dari frontier
        node = frontier.remove()

        # Langkah 3 GRAPH-SEARCH, goal test saat node dikeluarkan
        if node.state == goal:
            if include_goal_in_explored:
                explored_order.append(node.state)
            path = build_path(node)
            trace_rows.append(
                make_trace_row(node.state + " (GOAL)", frontier, explored_order)
            )
            break

        # Langkah 4 GRAPH-SEARCH, masukkan node ke explored set
        explored_set.add(node.state)
        explored_order.append(node.state)

        # Langkah 5 GRAPH-SEARCH, ekspansi node, anak hanya ditambahkan kalau
        # belum ada di frontier atau explored set
        new_neighbor_states = []
        for neighbor in sorted(graph[node.state]):
            already_in_frontier = frontier.contains_state(neighbor)
            already_explored = neighbor in explored_set
            if not already_in_frontier and not already_explored:
                new_neighbor_states.append(neighbor)

        if frontier.add_children_in_reverse_order:
            new_neighbor_states.reverse()

        for neighbor in new_neighbor_states:
            frontier.add(Node(neighbor, parent=node))

        trace_rows.append(make_trace_row(node.state, frontier, explored_order))

    if trace:
        print_trace_table(frontier, trace_rows)

    return path, explored_order


def build_path(goal_node):
    """Telusuri parent dari goal sampai start, lalu balik urutannya."""
    path = []
    current_node = goal_node
    while current_node is not None:
        path.append(current_node.state)
        current_node = current_node.parent
    path.reverse()
    return path


# Fungsi bantu untuk mencetak tabel trace

STEP_COLUMN_WIDTH = 7
REMOVED_COLUMN_WIDTH = 26
FRONTIER_COLUMN_WIDTH = 38
EXPLORED_COLUMN_WIDTH = 38


def make_trace_row(removed_label, frontier, explored_order):
    frontier_states = []
    for node in frontier.nodes:
        frontier_states.append(node.state)
    # Disalin karena explored_order masih terus bertambah setelah langkah ini
    explored_so_far = list(explored_order)
    return {
        "removed": removed_label,
        "frontier": frontier_states,
        "explored": explored_so_far,
    }


def split_names_into_lines(names, max_line_length):
    """Bagi daftar nama ke beberapa baris tanpa memotong nama di tengah."""
    lines = []
    current_line = ""
    for name in names:
        if current_line == "":
            current_line = name
            continue
        line_if_name_added = current_line + ", " + name
        # +1 karena baris yang dipotong diberi koma di akhirnya
        if len(line_if_name_added) + 1 > max_line_length:
            lines.append(current_line + ",")
            current_line = name
        else:
            current_line = line_if_name_added
    lines.append(current_line)
    return lines


def get_line_or_blank(lines, line_number):
    if line_number < len(lines):
        return lines[line_number]
    return ""


def print_table_row(step_text, removed_text, frontier_names, explored_names):
    step_lines = [step_text]
    removed_lines = [removed_text]
    frontier_lines = split_names_into_lines(frontier_names, FRONTIER_COLUMN_WIDTH)
    explored_lines = split_names_into_lines(explored_names, EXPLORED_COLUMN_WIDTH)

    # Kolom langkah dan kolom dikeluarkan selalu satu baris,
    # jadi tinggi baris ditentukan oleh kolom frontier dan explored
    row_height = max(len(frontier_lines), len(explored_lines))
    for line_number in range(row_height):
        step_part = get_line_or_blank(step_lines, line_number).ljust(STEP_COLUMN_WIDTH)
        removed_part = get_line_or_blank(removed_lines, line_number).ljust(
            REMOVED_COLUMN_WIDTH
        )
        frontier_part = get_line_or_blank(frontier_lines, line_number).ljust(
            FRONTIER_COLUMN_WIDTH
        )
        explored_part = get_line_or_blank(explored_lines, line_number).ljust(
            EXPLORED_COLUMN_WIDTH
        )
        full_line = (
            step_part
            + " | "
            + removed_part
            + " | "
            + frontier_part
            + " | "
            + explored_part
        )
        print(full_line.rstrip())


def make_separator_line():
    step_dashes = "-" * STEP_COLUMN_WIDTH
    removed_dashes = "-" * REMOVED_COLUMN_WIDTH
    frontier_dashes = "-" * FRONTIER_COLUMN_WIDTH
    explored_dashes = "-" * EXPLORED_COLUMN_WIDTH
    return (
        step_dashes
        + "-+-"
        + removed_dashes
        + "-+-"
        + frontier_dashes
        + "-+-"
        + explored_dashes
    )


def print_trace_table(frontier, trace_rows):
    if isinstance(frontier, QueueFrontier):
        print("Frontier berupa antrian, elemen paling kiri adalah depan antrian.")
    else:
        print("Frontier berupa stack, elemen paling kanan adalah puncak stack.")

    separator_line = make_separator_line()
    print(separator_line)
    print_table_row("Langkah", "Dikeluarkan", ["Frontier"], ["Explored"])
    print(separator_line)

    step_number = 1
    for row in trace_rows:
        frontier_names = row["frontier"]
        if len(frontier_names) == 0:
            frontier_names = ["(kosong)"]
        explored_names = row["explored"]
        if len(explored_names) == 0:
            explored_names = ["(kosong)"]
        print_table_row(
            str(step_number), row["removed"], frontier_names, explored_names
        )
        step_number += 1

    print(separator_line)
