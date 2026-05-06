import itertools
import subprocess
import os

nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
node_to_int = {node: i + 1 for i, node in enumerate(nodes)}
edges = [
    ('A', 'B'), ('A', 'G'), ('A', 'H'), ('B', 'C'), ('B', 'I'),
    ('C', 'K'), ('C', 'D'), ('D', 'E'), ('D', 'K'), ('E', 'F'),
    ('E', 'L'), ('F', 'G'), ('F', 'L'), ('G', 'H'), ('H', 'J'),
    ('I', 'J'), ('I', 'K'), ('J', 'L')
]

def run_minisat(k):
    clauses = []
    
    # RULE 1: Every edge must be covered (u OR v)
    for u, v in edges:
        clauses.append([node_to_int[u], node_to_int[v]])
    
    # RULE 2: At most k vertices (The Fix)
    # We forbid any combination of k + 1 vertices from being all True.
    # Logic: (NOT v1 OR NOT v2 OR ... OR NOT vk+1)
    for combo in itertools.combinations(nodes, k + 1):
        clauses.append([-node_to_int[n] for n in combo])

    # Write DIMACS file
    with open("vertex_cover.cnf", "w") as f:
        f.write(f"p cnf {len(nodes)} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")

    try:
        subprocess.run(['minisat', 'vertex_cover.cnf', 'problem1c.txt'], capture_output=True, text=True)
    except FileNotFoundError:
        return "MINISAT NOT FOUND", []
    
    if not os.path.exists("problem1c.txt"): return "ERROR", []
    
    with open("problem1c.txt", "r") as f:
        result = f.readline().strip()
        if result == "SAT":
            assignment = f.readline().split()
            # MiniSat outputs literals; positive means the node is in the cover
            selected = [nodes[int(x)-1] for x in assignment if int(x) > 0]
            return "SAT", selected
    return "UNSAT", []

# 2. Main Loop
try:
    start_k = int(input("Enter start of range: "))
    end_k = int(input("Enter end of range: "))

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