import hashlib
import hmac
import struct
import time
import networkx as nx
import random

def generate_totp_sha256(secret, digits, time_step=5):
    # Parameters: 
    # secret (bytes) sbg kata kunci, 
    # time_step (int) dalam satuan detik, 
    # digits (int) banyaknya digit otp yang akan dihasilkan

    # Hitung time step terkini
    current_time_step = int(time.time() / time_step)

    # Ubah time step menjadi byte array (big-endian)
    time_step_bytes = struct.pack(">Q", current_time_step)

    # Hitung nilai HMAC menggunakan SHA-256
    hmac_digest = hmac.new(secret, time_step_bytes, hashlib.sha256).digest()

    # Dynamic Truncation, ekstraksi 4 bytes dari nilai HMAC
    offset = hmac_digest[-1] & 0x0F
    truncated_hash = hmac_digest[offset : offset + 4]

    # Ubah hasil menjadi bentuk integer
    otp_value = struct.unpack(">I", truncated_hash)[0]

    # Ambil sebanyak digit yang diinginkan
    totp = otp_value % 10 ** digits

    # Formatting jika angka awal berupa '0'
    return f"{totp:0{digits}}"

def generate_weighted_complete_graph(num_nodes, min_weight, max_weight):
    G = nx.complete_graph(num_nodes)

    # Generate bobot pada tiap sisi yang ada menggunaakn library random
    weighted_edges = [(u, v, random.randint(min_weight, max_weight)) for u, v in G.edges]
    G.add_weighted_edges_from(weighted_edges)
    return G

def is_hamiltonian_path(graph, path):
    # Menguji apakah sebuah jalur masukan 'path' berupa hamilton, 
    # dengan memastikan simpul yang dilewati tepat sastu kali menggunakan fungsi set,
    # serta memerikasa setiap simpul u dan v terhubung di graph
    return set(path) == set(graph.nodes) and all(u in graph[v] for u, v in zip(path, path[1:]))

def find_random_hamiltonian_path(graph):
    # Membuat daftar simpul dalam graf
    nodes = list(graph.nodes)

    # Mengacak urutan simpul
    random.shuffle(nodes)

    # Iterasi melalui semua permutasi simpul
    for path in [nodes[i:] + nodes[:i] for i in range(len(nodes))]:
        # Memeriksa apakah jalur yang dihasilkan memenuhi kriteria jalur Hamiltonian
        if is_hamiltonian_path(graph, path):
            return path  # Jalur Hamiltonian ditemukan
    return None  # Tidak ada jalur Hamiltonian dalam graf

def list_to_integer(digits):
    # Pastikan digits berisi angka-angka
    if not all(isinstance(digit, int) for digit in digits):
        raise ValueError("Semua elemen dalam list harus berupa integer.")

    # Menggabungkan digit menjadi satu bilangan integer
    result = int("".join(map(str, digits)))
    return result

def generate_hamilton_code(num_nodes, min_weight, max_weight):
    # Generate graph dari masukan fungsi
    weighted_graph = generate_weighted_complete_graph(num_nodes, min_weight, max_weight)

    # Mencari jalur hamilton
    hamiltonian_path = find_random_hamiltonian_path(weighted_graph)

    # Mengubah hasil hamilton yang dalam bentuk list menjadi integer 6 digit
    hamilton_10digits = list_to_integer(hamiltonian_path)
    hamilton = hamilton_10digits % 10 ** 6

    # Mencari total bobot sisi yang dilalui siklus hamilton
    total_weight = 0
    if hamiltonian_path:
        for i in range(len(hamiltonian_path)):
            node = hamiltonian_path[i]
            next_node = hamiltonian_path[(i + 1) % len(hamiltonian_path)] 
            edge_weight = weighted_graph[int(node)][int(next_node)]['weight']
            total_weight += edge_weight
    else:
        print("Tidak ada jalur Hamilton yang ditemukan.")
    return f"{hamilton:0{digits}}", total_weight

def combine_digits(number1, number2, modulus_value):
    # Ambil digit pertama dari number1 sebanyak hasil modulus dan sisa digit terakhir dari number2
    result = int(str(number1)[:modulus_value] + str(number2)[modulus_value:])
    return result

if __name__ == "__main__":
    # Banyak digit yang akan dihasilkan
    digits = 6

    # Secret key, harus dirahasiakan
    secret_key = b"MySecretKey123"

    # Generate TOTP menggunakan SHA-256
    totp = generate_totp_sha256(secret_key, digits)

    # Definisikan banyak nodes dan rentang bobot sisi dalam graf yang akan digenerate
    num_nodes = 10
    min_weight = 0
    max_weight = 9

    # Generate kode hamilton
    hamilton = generate_hamilton_code(num_nodes, min_weight, max_weight)

    # Fungsi generate_hamilton_code mengembalikan tuple kode hamilton dan total bobot yang dilalui
    hamilton_code, total_weight = hamilton

    # Mencari nilai modulus dari total bobot
    modulus_value = 0
    while (modulus_value == 0):
        modulus_value = total_weight % 6
        total_weight = total_weight + 1

    # Mencari dan mencetak hasil akhir dari kombinasi kedua algoritma
    result = combine_digits(f"{totp:0{digits}}", f"{hamilton_code:0{digits}}", modulus_value)
    print("Kode OTP dari algoritma TOTP                                : " + str(totp))
    print("Kode OTP dari algoritma Graf Hamilton                       : " + str(hamilton_code))
    print("Nilai modulus dari total bobot yang dilalui siklus hamilton : " + str(modulus_value))
    print("Hasil OTP kombinasi TOTP dan Graf Hamilton                  : " + str(result))


