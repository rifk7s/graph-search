import unittest

from core.graphs import PAGE08, ROUTE_HOME_TO_UC
from core.search import Node, QueueFrontier, StackFrontier, graph_search


class TestFrontier(unittest.TestCase):
    def test_stack_frontier_removes_last_added_node(self):
        stack = StackFrontier()
        stack.add(Node("A"))
        stack.add(Node("B"))
        stack.add(Node("C"))
        removed_node = stack.remove()
        self.assertEqual(removed_node.state, "C")

    def test_queue_frontier_removes_first_added_node(self):
        queue = QueueFrontier()
        queue.add(Node("A"))
        queue.add(Node("B"))
        queue.add(Node("C"))
        removed_node = queue.remove()
        self.assertEqual(removed_node.state, "A")


class TestPage08(unittest.TestCase):
    def test_bfs(self):
        path, explored_order = graph_search(
            "Denpasar", "Padangbai", QueueFrontier(), PAGE08
        )
        expected_path = ["Denpasar", "Mengwi", "Ubud", "Padangbai"]
        expected_explored_order = [
            "Denpasar",
            "Kuta",
            "Mengwi",
            "Ngerebong",
            "Ubud",
            "Sukawati",
        ]
        self.assertEqual(path, expected_path)
        self.assertEqual(explored_order, expected_explored_order)

    def test_dfs(self):
        path, explored_order = graph_search(
            "Denpasar", "Padangbai", StackFrontier(), PAGE08
        )
        expected_path = ["Denpasar", "Mengwi", "Ubud", "Padangbai"]
        expected_explored_order = ["Denpasar", "Kuta", "Mengwi", "Ubud"]
        self.assertEqual(path, expected_path)
        self.assertEqual(explored_order, expected_explored_order)

    def test_include_goal_in_explored(self):
        path, explored_order = graph_search(
            "Denpasar",
            "Padangbai",
            QueueFrontier(),
            PAGE08,
            include_goal_in_explored=True,
        )
        expected_path = ["Denpasar", "Mengwi", "Ubud", "Padangbai"]
        expected_explored_order = [
            "Denpasar",
            "Kuta",
            "Mengwi",
            "Ngerebong",
            "Ubud",
            "Sukawati",
            "Padangbai",
        ]
        self.assertEqual(path, expected_path)
        self.assertEqual(explored_order, expected_explored_order)


class TestRouteHomeToUC(unittest.TestCase):
    def test_bfs(self):
        path, explored_order = graph_search(
            "Rumah", "UC Makassar", QueueFrontier(), ROUTE_HOME_TO_UC
        )
        expected_path = [
            "Rumah",
            "Jl. Tarakan",
            "Jl. Nusantara",
            "Jl. Riburane",
            "Jl. Ahmad Yani",
            "Jl. Kajaolalido",
            "Jl. Botolempangan",
            "Jl. Arief Rate",
            "Jl. H. Bau",
            "Jl. Metro Tj. Bunga",
            "UC Makassar",
        ]
        expected_explored_order = [
            "Rumah",
            "Jl. Tarakan",
            "Jl. Tentara Pelajar",
            "Jl. Nusantara",
            "Jl. Yos Sudarso",
            "Jl. Sarappo",
            "Jl. Riburane",
            "Jl. Andalas",
            "Jl. Ternate",
            "Jl. Ahmad Yani",
            "Jl. Gunung Latimojong",
            "Jl. Lembeh",
            "Jl. Kajaolalido",
            "Jl. G. Bawakaraeng",
            "Jl. KH Wahid Hasyim",
            "Jl. Botolempangan",
            "Jl. Jend. Sudirman",
            "Jl. HOS Cokroaminoto",
            "Jl. Arief Rate",
            "Jl. Ince Nurdin",
            "Jl. H. Bau",
            "Jl. Metro Tj. Bunga",
        ]
        self.assertEqual(path, expected_path)
        self.assertEqual(explored_order, expected_explored_order)

    def test_dfs(self):
        path, explored_order = graph_search(
            "Rumah", "UC Makassar", StackFrontier(), ROUTE_HOME_TO_UC
        )
        expected_path = [
            "Rumah",
            "Jl. Tarakan",
            "Jl. Nusantara",
            "Jl. Riburane",
            "Jl. Ahmad Yani",
            "Jl. Kajaolalido",
            "Jl. Botolempangan",
            "Jl. Arief Rate",
            "Jl. H. Bau",
            "Jl. Metro Tj. Bunga",
            "UC Makassar",
        ]
        expected_explored_order = [
            "Rumah",
            "Jl. Tarakan",
            "Jl. Nusantara",
            "Jl. Riburane",
            "Jl. Ahmad Yani",
            "Jl. Kajaolalido",
            "Jl. Botolempangan",
            "Jl. Arief Rate",
            "Jl. H. Bau",
            "Jl. Metro Tj. Bunga",
        ]
        self.assertEqual(path, expected_path)
        self.assertEqual(explored_order, expected_explored_order)


if __name__ == "__main__":
    unittest.main()
