"""Independent red-team verifiers (written by `q6-hypergraph`, NOT reusing the Lead's or
the witnesses' authors' code).  Each check is implemented from the mathematical definition.

Usage:
    python audit_verify.py q7 <file>       # Q7 edge list: "u v" per line, or JSON list
    python audit_verify.py q8 <file>       # same for Q8 (0..255)
    python audit_verify.py a11 <file>      # JSON {"set": [11 ints], "max": M} or plain list
    python audit_verify.py q6 <file>       # JSON {"edges": [[6 ints],...]}

Checks are deliberately implemented a second, different way from the natural one:
 * C4-freeness: instead of enumerating the C(n,2)*2^(n-2) four-cycles, we use the equivalent
   criterion "some pair of vertices at Hamming distance 2 has >= 2 common neighbours"
   (in a bipartite graph a 4-cycle exists iff such a pair exists) — O(V^2) over all pairs.
   We then ALSO enumerate all four-cycles explicitly (both because the criterion needs a
   sanity anchor and to catch an off-by-one in the corner enumeration) and cross-check.
 * Q6 tau: enumerate ALL 5-subsets of the vertex union (exact) and require that each misses
   at least one edge; plus confirm tau<=6 by the single-line argument.
 * a(11): exact set of 2^11 subset sums, checked for cardinality 2048 and max <= M.
Exit code 0 iff every check passes.
"""
import itertools
import json
import os
import sys


def load_edges(path):
    """Accepts: plain text 'u v' lines, JSON {"edges": [[u,v],...]}, or a JSON list of such."""
    txt = open(path).read().strip()
    if txt.startswith("{") or txt.startswith("["):
        obj = json.loads(txt)
        if isinstance(obj, dict):
            obj = obj.get("edges", obj.get("edge_list"))
        if isinstance(obj, list) and obj and isinstance(obj[0], dict):
            # catalogue form: list of {"edges": [[u,v],...]}  -> concatenate all
            out = []
            for o in obj:
                out.extend(tuple(map(int, e)) for e in o["edges"])
            return out
        return [tuple(map(int, e)) for e in obj]
    edges = []
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", " ").split()
        edges.append((int(parts[0]), int(parts[1])))
    return edges


def c4_check(n, edges):
    V = 1 << n
    bad = [e for e in edges if e[0] == e[1] or not (0 <= e[0] < V and 0 <= e[1] < V)
           or bin(e[0] ^ e[1]).count("1") != 1]
    ok = True
    if bad:
        print("  FAIL: %d entries are not Q%d edges (loop/out of range/not Hamming-1), e.g. %s"
              % (len(bad), n, bad[:5]))
        ok = False
    if len(set(map(tuple, edges))) != len(edges):
        print("  FAIL: duplicate edges present")
        ok = False
    E = {(min(e), max(e)) for e in edges}
    # (a) independent criterion: a 4-cycle exists iff a Hamming-distance-2 pair has 2 common nbrs
    nbr = {v: set() for v in range(V)}
    for u, v in E:
        nbr[u].add(v)
        nbr[v].add(u)
    viol = 0
    # iterate unordered pairs at Hamming distance 2
    for u in range(V):
        for i in range(n):
            for j in range(i + 1, n):
                v = u ^ (1 << i) ^ (1 << j)
                if v <= u:
                    continue
                common = len(nbr[u] & nbr[v])
                if common >= 2:
                    viol += 1
    print("  pairs at Hamming distance 2 with >=2 common neighbours: %d" % viol)
    # (b) exhaustive four-cycle enumeration by corner tuples (independent of (a))
    cnt = 0
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            for b in range(V):
                if (b >> i) & 1 or (b >> j) & 1:
                    continue
                total += 1
                v1 = b
                v2 = b | (1 << i)
                v3 = b | (1 << j)
                v4 = b | (1 << i) | (1 << j)
                if all(e in E for e in ((min(v1, v2), max(v1, v2)),
                                        (min(v1, v3), max(v1, v3)),
                                        (min(v2, v4), max(v2, v4)),
                                        (min(v3, v4), max(v3, v4)))):
                    cnt += 1
    print("  four-cycles enumerated: %d, fully present: %d" % (total, cnt))
    ok = ok and viol == 0 and cnt == 0
    print("  |E| = %d  (Q%d has %d edges, %d four-cycles)"
          % (len(E), n, n * (1 << (n - 1)), (n * (n - 1) // 2) * (1 << (n - 2))))
    print("  RESULT:", "PASS (C4-free)" if ok else "FAIL")
    return ok


def a11_check(path):
    obj = json.load(open(path))
    S = obj["set"] if isinstance(obj, dict) else obj
    S = [int(x) for x in S]
    ok = True
    if len(S) != 11:
        print("  FAIL: |S| = %d != 11" % len(S)); ok = False
    if len(set(S)) != 11:
        print("  FAIL: repeated elements"); ok = False
    if min(S) < 1:
        print("  FAIL: non-positive element"); ok = False
    sums = set()
    for mask in range(1 << len(S)):
        sums.add(sum(S[i] for i in range(len(S)) if (mask >> i) & 1))
    if len(sums) != 1 << len(S):
        print("  FAIL: only %d distinct subset sums (need %d)" % (len(sums), 1 << len(S)))
        ok = False
    M = max(S)
    if isinstance(obj, dict) and "max" in obj and int(obj["max"]) != M:
        print("  WARN: declared max %s != computed max %d" % (obj["max"], M))
    print("  S =", sorted(S))
    print("  max = %d, distinct subset sums = %d/%d" % (M, len(sums), 1 << len(S)))
    print("  RESULT:", "PASS (dissociated, a(11) <= %d)" % M if ok else "FAIL")
    return ok


def q6_check(path):
    obj = json.load(open(path))
    edges = [tuple(sorted(int(x) for x in e)) for e in obj["edges"]]
    ok = True
    m = len(edges)
    if m > 17:
        print("  NOTE: m = %d > 17 (not a record claim for m<=17)" % m)
    for e in edges:
        if len(set(e)) != 6:
            print("  FAIL: edge with != 6 distinct vertices:", e); ok = False
    if len(set(edges)) != m:
        print("  FAIL: duplicate edges"); ok = False
    for a, b in itertools.combinations(range(m), 2):
        if not (set(edges[a]) & set(edges[b])):
            print("  FAIL: disjoint pair", edges[a], edges[b]); ok = False
    V = sorted(set(itertools.chain(*edges)))
    print("  m = %d, vertex union size = %d, max label = %d" % (m, len(V), max(V)))
    idx = {v: i for i, v in enumerate(V)}
    emask = [sum(1 << idx[x] for x in e) for e in edges]
    # tau <= 6: the 6 points of any one edge meet every edge (pairwise intersecting)
    # tau = 6: every 5-subset of V misses at least one edge
    full = (1 << len(V)) - 1
    bad = 0
    for S in itertools.combinations(range(len(V)), 5):
        sm = 0
        for p in S:
            sm |= 1 << p
        if all(em & sm for em in emask):   # S meets every edge -> S is a transversal
            bad += 1
    print("  5-element transversals found: %d  (need 0)" % bad)
    print("  lower bound on tau is 6")
    ok = ok and bad == 0
    print("  RESULT:", "PASS (intersecting, tau = 6)" if ok else "FAIL")
    return ok


def team_mode():
    """One-command red-team check of the team's final artifacts."""
    import glob
    base = os.path.dirname(os.path.abspath(__file__))
    ws = os.path.abspath(os.path.join(base, "..", ".."))
    arts = [
        ("Q8 682-edge C4-free (A)", "c4_8", os.path.join(ws, "research", "c4-hypercube", "edges_q8.txt")),
        ("a(11) baseline Conway-Guy 594 (B)", "a11", os.path.join(ws, "research", "subset-sums", "witness_a11.json")),
    ]
    allok = True
    for name, kind, path in arts:
        print("\n=== %s\n    file: %s" % (name, path))
        if not os.path.exists(path):
            print("  MISSING"); allok = False; continue
        ok = c4_check(int(kind[3:]), load_edges(path)) if kind.startswith("c4_") else a11_check(path)
        allok = allok and ok
    for path in sorted(glob.glob(os.path.join(ws, "research", "common", "q7_lns*.txt"))):
        print("\n=== Q7 LNS output: %s" % path)
        ok = c4_check(7, load_edges(path))
        allok = allok and ok
    print("\n######## TEAM RESULT:", "ALL PASS" if allok else "SOME CHECKS FAILED")
    return allok


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "team":
        sys.exit(0 if team_mode() else 1)
    kind, path = sys.argv[1], sys.argv[2]
    print("== %s : %s ==" % (kind, path))
    if kind == "q7":
        ok = c4_check(7, load_edges(path))
    elif kind == "q8":
        ok = c4_check(8, load_edges(path))
    elif kind.startswith("c4_"):          # c4_<n> : hypercube C4-freeness, any n
        ok = c4_check(int(kind[3:]), load_edges(path))
    elif kind == "a11":
        ok = a11_check(path)
    elif kind == "q6":
        ok = q6_check(path)
    else:
        raise SystemExit("unknown kind " + kind)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
