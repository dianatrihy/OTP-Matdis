import hashlib
import hmac
import struct
import time
import networkx as nx
import random

def generate_weighted_complete_graph(num_nodes, min_weight, max_weight):
    G = nx.complete_graph(num_nodes)
    weighted_edges = [(u, v, random.randint(min_weight, max_weight)) for u, v in G.edges]
    G.add_weighted_edges_from(weighted_edges)
    return G

def is_hamiltonian_path(graph, path):
    return set(path) == set(graph.nodes) and all(u in graph[v] for u, v in zip(path, path[1:]))

def find_random_hamiltonian_path(graph):
    nodes = list(graph.nodes)
    random.shuffle(nodes)
    for path in [nodes[i:] + nodes[:i] for i in range(len(nodes))]:
        if is_hamiltonian_path(graph, path):
            return path
    return None

def generate_totp_sha256(secret, time_step=5, digits=6):
    """
    Generate Time-based One-Time Password (TOTP) using SHA-256.

    Parameters:
    - secret (bytes): Secret key used for HMAC.
    - time_step (int): Time step in seconds. Default is 30 seconds.
    - digits (int): Number of digits in the OTP. Default is 6.

    Returns:
    - str: Generated TOTP.
    """
    # Calculate the current time step
    current_time_step = int(time.time() / time_step)
    print(current_time_step)
    print("\n")

    # Convert the time step to a byte array (big-endian)
    time_step_bytes = struct.pack(">Q", current_time_step)
    print(time_step_bytes)
    print("\n")

    # Calculate HMAC using SHA-256
    hmac_digest = hmac.new(secret, time_step_bytes, hashlib.sha256).digest()
    print(hmac_digest)
    print("\n")

    # Dynamic Truncation: Extract 4 bytes from the HMAC value
    offset = hmac_digest[-1] & 0x0F
    truncated_hash = hmac_digest[offset : offset + 4]
    print(truncated_hash)
    print("\n")

    # Convert the result to an integer
    otp_value = struct.unpack(">I", truncated_hash)[0]
    print(otp_value)
    print("\n")

    # Only keep the last 'digits' digits
    totp = otp_value % 10 ** digits

    # Format the TOTP to have leading zeros if needed
    return f"{totp:0{digits}}"

# Example Usage:
if __name__ == "__main__":
    # Secret key (should be kept secret and shared between the server and the user)
    secret_key = b"MySecretKey123"

    # Generate TOTP using SHA-256
    totp = generate_totp_sha256(secret_key)

    # Print the generated TOTP
    print(f"Generated TOTP: {totp}")

    num_nodes = 10
    min_weight = 0
    max_weight = 9

    # Generate a weighted complete graph with weights from the specified range
    weighted_graph = generate_weighted_complete_graph(num_nodes, min_weight, max_weight)

    # Find a Hamiltonian path with weights
    hamiltonian_path = find_random_hamiltonian_path(weighted_graph)
    print(hamiltonian_path)

    if hamiltonian_path:
        # Print the Hamiltonian path with weights
        for i in range(len(hamiltonian_path)):
            node = hamiltonian_path[i]
            next_node = hamiltonian_path[(i + 1) % len(hamiltonian_path)]  # Ensure it wraps around

            edge_weight = weighted_graph[int(node)][int(next_node)]['weight']
            print(f"Edge: {node} - {next_node}, Weight: {edge_weight}")
    else:
        print("Tidak ada jalur Hamiltonian yang ditemukan.")
