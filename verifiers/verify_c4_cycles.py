#!/usr/bin/env python3
"""Independent verifier for C4-free subgraphs of Q_n (n=7 or 8).

Usage:  python verify_q7.py [edges_file] [--n N]
Default file: edges_q7.txt (in same directory), n=7; for q8 pass --n 8 and edges_q8.txt.

Edge encoding: each line "u v" with 0 <= u < v < 2^n and popcount(u^v) == 1.
It checks:
  1. every line is a genuine hypercube edge (Hamming distance exactly 1),
  2. no duplicate edges,
  3. no 4-cycle (square) of Q_n is fully contained in the edge set,
  4. prints the number of kept edges, the number of 4-cycles, and "VERIFIED n".

4-cycles of Q_n: for every pair of coordinates {i,j} and every assignment of the other
n-2 coordinates, the four edges of the resulting square.
"""
import sys, itertools

def popcount(x):
    return bin(x).count("1")

def hypercube_edges(n):
    E = set()
    for u in range(1 << n):
        for i in range(n):
            v = u ^ (1 << i)
            E.add((min(u, v), max(u, v)))
    return E

def four_cycles(n):
    """Yield each 4-cycle as a frozenset of 4 edge pairs."""
    cycles = []
    others = list(range(n))
    for i, j in itertools.combinations(range(n), 2):
        rest = [k for k in range(n) if k != i and k != j]
        for assign in itertools.product([0, 1], repeat=len(rest)):
            base = 0
            for k, b in zip(rest, assign):
                base |= b << k
            v00 = base
            v10 = base | (1 << i)
            v01 = base | (1 << j)
            v11 = base | (1 << i) | (1 << j)
            e = [(min(a, b), max(a, b)) for a, b in
                 [(v00, v10), (v00, v01), (v11, v10), (v11, v01)]]
            cycles.append(frozenset(e))
    return cycles

def verify(edges, n):
    E = hypercube_edges(n)
    kept = set()
    for idx, (u, v) in enumerate(edges):
        if not (0 <= u < v < (1 << n)):
            return None, f"line {idx}: bad range {u} {v}"
        if popcount(u ^ v) != 1:
            return None, f"line {idx}: ({u},{v}) is not a Q{n} edge (weight {popcount(u^v)})"
        if (u, v) in kept:
            return None, f"line {idx}: duplicate edge ({u},{v})"
        if (u, v) not in E:
            return None, f"line {idx}: edge not in Q{n}"
        kept.add((u, v))
    cycles = four_cycles(n)
    seen = set()
    for c in cycles:
        if c in seen:
            continue
        seen.add(c)
        if c <= kept:
            return None, f"4-cycle present: {sorted(c)}"
    return len(kept), f"VERIFIED n={n} kept={len(kept)} cycles={len(seen)}"

def load(path):
    edges = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.replace(",", " ").split()
            if len(parts) != 2:
                raise ValueError(f"bad line: {line!r}")
            edges.append((int(parts[0]), int(parts[1])))
    return edges

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    n = 7
    path = None
    i = 0
    while i < len(args):
        if args[i] == "--n":
            n = int(args[i + 1]); i += 2
        else:
            path = args[i]; i += 1
    if path is None:
        path = "edges_q%d.txt" % n
    edges = load(path)
    count, msg = verify(edges, n)
    print(msg)
    sys.exit(0 if count is not None else 1)
