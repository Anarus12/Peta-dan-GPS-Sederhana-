import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# Data kota dan jarak antar kota (Km)
Kotakuy = [
    ("Los Angeles", "Chicago", 3242),
    ("Los Angeles", "Dallas", 2311),
    ("Los Angeles", "Phoenix", 598),
    ("Los Angeles", "San Antonio", 2175),
    ("Los Angeles", "San Diego", 193),

    ("San Diego", "Phoenix", 569),
    ("San Diego", "Austin", 2090),
    ("San Diego", "Houston", 2365),
    ("San Diego", "San Antonio", 2050),

    ("Phoenix", "New York City", 3873),
    ("Phoenix", "Chicago", 2822),
    ("Phoenix", "Dallas", 1717),
    ("Phoenix", "Austin", 1622),
    ("Phoenix", "San Antonio", 1581),

    ("San Antonio", "Dallas", 440),
    ("San Antonio", "Austin", 127),
    ("San Antonio", "Houston", 317),

    ("Houston", "Austin", 260),
    ("Houston", "Dallas", 384),
    ("Houston", "Chicago", 1741),
    ("Houston", "Philadelphia", 2484),
    ("Houston", "New York City", 2628),

    ("Austin", "Philadelphia", 2669),
    ("Austin", "Dallas", 313),

    ("Dallas", "Philadelphia", 2360),
    ("Dallas", "New York City", 2500),
    ("Dallas", "Chicago", 1490),

    ("Philadelphia", "New York City", 157),
    ("Philadelphia", "Chicago", 1223),

    ("New York City", "Chicago", 1281),
]

# Daftar jenis transportasi dan koefisien waktu tempuh (semakin besar = lebih lambat)
transport_modes = {
    "mobil": 1,
    "bus": 1.2,
    "pesawat": 0.5
}

# Fungsi membuat graph sesuai transportasi
def buat_graph(transportasi):
    factor = transport_modes.get(transportasi.lower(), 1)
    G = nx.Graph()
    for u, v, w in Kotakuy:
        G.add_edge(u, v, weight=w * factor)
    return G

# Visualisasi
def tampilkan_graph(G):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    rounded_labels = {k: f"{v:.0f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=rounded_labels)
    plt.title("Graph Peta Antar Kota (Transportasi disesuaikan)")
    plt.show()

# Dijkstra
def shortest_path_dijkstra(G, start, end):
    try:
        path = nx.dijkstra_path(G, start, end)
        length = nx.dijkstra_path_length(G, start, end)
        print(f"\nJalur tercepat dari {start} ke {end}:")
        print(" -> ".join(path))
        print(f"Total jarak/tempuh setelah faktor transportasi: {length:.2f} Km (waktu relatif)")
    except nx.NetworkXNoPath:
        print("Tidak ada jalur yang tersedia antara kota tersebut.")
    except nx.NodeNotFound:
        print("Nama kota tidak ditemukan dalam graph.")

# TSP Brute Force
def tsp_brute_force(G):
    cities = list(G.nodes)
    min_path = None
    min_distance = float('inf')

    for perm in permutations(cities):
        distance = 0
        valid = True
        for i in range(len(perm) - 1):
            if G.has_edge(perm[i], perm[i+1]):
                distance += G[perm[i]][perm[i+1]]['weight']
            else:
                valid = False
                break
        if valid and distance < min_distance:
            min_distance = distance
            min_path = perm

    if min_path:
        print("\nRute TSP terbaik (brute-force):")
        print(" -> ".join(min_path))
        print(f"Total jarak/tempuh: {min_distance:.2f} Km (waktu relatif)")
    else:
        print("Tidak ada rute TSP yang valid")

# Menu interaktif
def menu():
    while True:
        print("\n===== MENU PROGRAM =====")
        print("1. Tampilkan visualisasi graph")
        print("2. Cari jalur tercepat (Dijkstra)")
        print("3. Cari rute optimal TSP (brute-force)")
        print("4. Keluar")

        pilihan = input("Masukkan pilihan (1-4): ")

        if pilihan in ["1", "2", "3"]:
            print("\nPilih jenis transportasi: mobil / bus / pesawat")
            jenis = input("Transportasi: ").lower()
            if jenis not in transport_modes:
                print("Jenis transportasi tidak valid. Default: mobil")
                jenis = "mobil"
            G = buat_graph(jenis)

            if pilihan == "1":
                tampilkan_graph(G)
            elif pilihan == "2":
                print("\nDaftar kota:", ', '.join(G.nodes))
                start = input("Masukkan kota awal: ")
                end = input("Masukkan kota tujuan: ")
                shortest_path_dijkstra(G, start, end)
            elif pilihan == "3":
                print("\n[PERHATIAN] Proses TSP brute-force bisa lama.")
                if input("Lanjutkan? (y/n): ").lower() == 'y':
                    tsp_brute_force(G)

        elif pilihan == "4":
            print("Terima kasih telah menggunakan program ini!")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1 - 4.")

# Jalankan program
menu()
