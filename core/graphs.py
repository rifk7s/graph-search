"""
Graf tanpa bobot dalam bentuk dict adjacency (undirected).
"""


def build_undirected_graph(edges):
    """Ubah daftar edge menjadi dict adjacency dua arah."""
    graph = {}
    for place_a, place_b in edges:
        if place_a not in graph:
            graph[place_a] = []
        if place_b not in graph:
            graph[place_b] = []
        graph[place_a].append(place_b)
        graph[place_b].append(place_a)
    return graph


# Rute dari Rumah ke Kampus UC Makassar
# Rumah adalah titik awal, alamat lengkap sengaja tidak dicantumkan
# UC Makassar : Ciputra School of Business, CitraLand City CPI, Jalan Sunset Boulevard, Makassar 90224
# Disusun dari petunjuk arah Google Maps untuk tiga rute.
# Bundaran dan belokan tanpa nama jalan tidak dijadikan node.
ROUTE_HOME_TO_UC = build_undirected_graph(
    [
        # Rute A via Jl. Nusantara (Google Maps 6,6 km, 18 menit)
        ("Rumah", "Jl. Tarakan"),
        ("Jl. Tarakan", "Jl. Nusantara"),
        ("Jl. Nusantara", "Jl. Riburane"),
        ("Jl. Riburane", "Jl. Ahmad Yani"),
        ("Jl. Ahmad Yani", "Jl. Kajaolalido"),
        ("Jl. Kajaolalido", "Jl. Botolempangan"),
        ("Jl. Botolempangan", "Jl. Arief Rate"),
        ("Jl. Arief Rate", "Jl. H. Bau"),
        ("Jl. H. Bau", "Jl. Metro Tj. Bunga"),
        ("Jl. Metro Tj. Bunga", "UC Makassar"),
        # Rute B via Jl. Andalas (6,6 km, 19 menit), edge yang sama dengan rute A tidak ditulis ulang
        ("Jl. Tarakan", "Jl. Yos Sudarso"),
        ("Jl. Yos Sudarso", "Jl. Andalas"),
        ("Jl. Andalas", "Jl. Gunung Latimojong"),
        ("Jl. Gunung Latimojong", "Jl. G. Bawakaraeng"),
        ("Jl. G. Bawakaraeng", "Jl. Jend. Sudirman"),
        ("Jl. Jend. Sudirman", "Jl. Ince Nurdin"),
        ("Jl. Ince Nurdin", "Jl. Botolempangan"),
        # Rute C via Jl. Sarappo (6,2 km, 20 menit), edge yang sama dengan rute A dan B tidak ditulis ulang.
        # Jl. Lae-Lae tidak dijadikan node karena di Google Maps hanya disebut sebagai arah
        # ("Head toward Jl. Lae-Lae"), lalu rute langsung belok ke Jl. Tentara Pelajar.
        ("Rumah", "Jl. Tentara Pelajar"),
        ("Jl. Tentara Pelajar", "Jl. Sarappo"),
        ("Jl. Sarappo", "Jl. Ternate"),
        ("Jl. Ternate", "Jl. Lembeh"),
        ("Jl. Lembeh", "Jl. KH Wahid Hasyim"),
        ("Jl. KH Wahid Hasyim", "Jl. HOS Cokroaminoto"),
        ("Jl. HOS Cokroaminoto", "Jl. Jend. Sudirman"),
    ]
)

# Graf soal Page 08 (Bali), dipakai untuk validasi hasil
PAGE08 = build_undirected_graph(
    [
        ("Kuta", "Denpasar"),
        ("Denpasar", "Ngerebong"),
        ("Denpasar", "Mengwi"),
        ("Ngerebong", "Ubud"),
        ("Ngerebong", "Sukawati"),
        ("Mengwi", "Ubud"),
        ("Ubud", "Padangbai"),
        ("Sukawati", "Padangbai"),
    ]
)
