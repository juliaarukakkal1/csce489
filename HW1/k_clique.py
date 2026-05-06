import itertools
import subprocess
import os

nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
node_to_int = {node: i + 1 for i, node in enumerate(nodes)}
edges = [
    ('A', 'C'), ('A', 'E'), ('B', 'H'), ('B', 'C'), ('B', 'D'),
    ('C', 'F'), ('C', 'D'), ('C', 'E'), ('D', 'E'), ('D', 'F'),
    ('E', 'F'), ('E', 'I'), ('E', 'G'), ('F', 'H'), ('F', 'G'),
    ('G', 'H'), ('G', 'I'), ('I', 'H')
]

def run_minisat(k):
    clauses = []

    adj = {n: set() for n in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # RULE 1: Cannot include 2 vertices without edge
    for u, v in itertools.combinations(nodes, 2):
        if v not in adj[u]:
            clauses.append([-node_to_int[u], -node_to_int[v]])
    
    
    # RULE 2: At least k vertices
    # To force 'at least k', we forbid any group of (n - k + 1) from all being False.
    n = len(nodes)
    for combo in itertools.combinations(nodes, n - k + 1):
        # Logic: (v1 OR v2 OR ... OR vn-k+1)
        clauses.append([node_to_int[n_var] for n_var in combo])

    # Write DIMACS file
    with open("k_clique.cnf", "w") as f:
        f.write(f"p cnf {len(nodes)} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")

    try:
        subprocess.run(['minisat', 'k_clique.cnf', 'result1c.txt'], capture_output=True, text=True)
    except FileNotFoundError:
        return "MINISAT NOT FOUND", []
    
    if not os.path.exists("result1c.txt"): return "ERROR", []
    

# 2. Main Loop
try:
    start_k = int(input("Enter start of k-clique range: "))
    end_k = int(input("Enter end of k-clique range: "))

    print(f"\n{'k':<5} | {'Result':<8} | {'Vertices'}")
    print("-" * 50)

    for k in range(start_k, end_k + 1):
        status, result_nodes = run_minisat(k)
        if status == "SAT":
            # Green text for SAT
            print(f"{k:<5} | \033[92m{status:<8}\033[0m | {', '.join(result_nodes)}")
        elif status == "UNSAT":
            # Red text for UNSAT
            print(f"{k:<5} | \033[91m{status:<8}\033[0m | None")
        else:
            print(f"{k:<5} | {status:<8} | N/A")
            
except ValueError:
    print("Please enter valid integers for k.")