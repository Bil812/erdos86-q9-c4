#!/usr/bin/env python3
"""Second, independent criterion for C4-freeness of a Q_n edge list (Lead's alt verifier).

Instead of enumerating 4-cycles, use the common-neighbour criterion:
a graph is C4-free iff every pair of vertices has at most one common neighbour.
For Q_n, only pairs at Hamming distance 2 can have 2 common neighbours; we count
codegrees over all pairs at distance 2 (and also check all other pairs trivially).

Usage: python verify_c4_alt.py edges.txt --n 9
"""
import sys, argparse
from collections import defaultdict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--n", type=int, default=9)
    a = ap.parse_args()
    n = a.n
    V = 1 << n
    adj = [set() for _ in range(V)]
    ne = 0
    with open(a.path) as f:
        for line in f:
            if not line.strip():
                continue
            u, v = map(int, line.split())
            assert 0 <= u < v < V, (u, v)
            assert bin(u ^ v).count("1") == 1, (u, v)
            assert v not in adj[u], "duplicate"
            adj[u].add(v); adj[v].add(u); ne += 1
    # codegree for pairs at Hamming distance 2 (only possible common neighbours)
    import itertools
    bad = 0
    pairs = 0
    seen = set()
    for u in range(V):
        for d1, d2 in itertools.combinations(range(n), 2):
            v = u ^ (1 << d1) ^ (1 << d2)
            if u < v:
                key = (u, v)
                if key in seen:
                    continue
                seen.add(key)
                pairs += 1
                common = len(adj[u] & adj[v])
                if common >= 2:
                    bad += 1
    print(f"edges={ne} distance-2 pairs={pairs} pairs_with_>=2_common_neighbours={bad}")
    print("VERIFIED (common-neighbour criterion)" if bad == 0 else "INVALID")
    return 0 if bad == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
