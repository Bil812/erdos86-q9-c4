# -*- coding: utf-8 -*-
"""Lead's independent verifier for a Q_n C4-free edge certificate.
Deliberately simple and self-contained; does not reuse the team's verifiers.
Usage: python verify_q9.py <edges_file> [n]
"""
import sys
from itertools import combinations


def main():
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    V = 1 << n

    edges = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                print(f"FAIL line {lineno}: not two integers: {line!r}")
                return 1
            u, v = int(parts[0]), int(parts[1])
            if not (0 <= u < v < V):
                print(f"FAIL line {lineno}: bad vertex range ({u},{v})")
                return 1
            if bin(u ^ v).count("1") != 1:
                print(f"FAIL line {lineno}: not a Q{n} edge ({u},{v})")
                return 1
            edges.append((u, v))

    eset = set(edges)
    if len(eset) != len(edges):
        print(f"FAIL duplicates: {len(edges)} lines, {len(eset)} distinct")
        return 1

    # Build adjacency
    adj = [set() for _ in range(V)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # Enumerate every 4-cycle (square face): pick 2 coords, fix other n-2 bits.
    faces = 0
    bad_faces = []
    edge_hist = {}
    for d1, d2 in combinations(range(n), 2):
        mask = (1 << d1) | (1 << d2)
        for base in range(V):
            if base & mask:
                continue  # canonical representative of the face
            a = base
            b = base ^ (1 << d1)
            c = base ^ (1 << d2)
            d = base ^ mask
            quad = [(a, b), (a, c), (d, b), (d, c)]
            cnt = sum(1 for (x, y) in quad if (min(x, y), max(x, y)) in eset)
            edge_hist[cnt] = edge_hist.get(cnt, 0) + 1
            faces += 1
            if cnt == 4:
                bad_faces.append((a, d1, d2))

    # Common-neighbour criterion: every pair has at most one common neighbour.
    bad_pairs = 0
    for u in range(V):
        for d1, d2 in combinations(range(n), 2):
            v = u ^ (1 << d1) ^ (1 << d2)
            if u < v and len(adj[u] & adj[v]) >= 2:
                bad_pairs += 1

    deg = {}
    for u in range(V):
        deg[len(adj[u])] = deg.get(len(adj[u]), 0) + 1
    dirs = [0] * n
    for u, v in edges:
        dirs[(u ^ v).bit_length() - 1] += 1

    print(f"n={n} vertices={V}")
    print(f"edges={len(edges)}  distinct={len(eset)}")
    print(f"4-cycles enumerated={faces} (expected C({n},2)*2^{n-2}={n*(n-1)//2 * (1 << (n-2))})")
    print(f"4-cycles with all 4 edges present={len(bad_faces)}")
    print(f"edge-count distribution over faces={dict(sorted(edge_hist.items()))}")
    print(f"pairs with >=2 common neighbours={bad_pairs}")
    print(f"degree distribution={dict(sorted(deg.items(), key=lambda t: str(t[0])))}")
    print(f"per-direction edge counts={dirs}")
    ok = (len(edges) > 0 and len(eset) == len(edges) and faces == n * (n - 1) // 2 * (1 << (n - 2))
          and len(bad_faces) == 0 and bad_pairs == 0)
    print("RESULT:", "VALID C4-FREE" if ok else "INVALID")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
