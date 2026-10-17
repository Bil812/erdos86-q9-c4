#!/usr/bin/env python3
"""Self-tests for the independent verifiers, on known values.

1) Q3: brute force all 2^12 edge subsets -> ex(Q3,C4) must equal 9 (OEIS A245762).
   Extract a max C4-free subgraph, write it, and check it through verify_q7 machinery (n=3).
2) A276661: the Conway-Guy 11-set must pass; a deliberately corrupted set must fail.
3) q6: PG(2,5) 31-line family must have tau=6 and be pairwise intersecting.
"""
import itertools, json, subprocess, sys

# ---------- Q3 brute force ----------
def popcount(x): return bin(x).count("1")

def hcube_edges(n):
    return [(u, u ^ (1 << i)) for u in range(1 << n) for i in range(n) if u < (u ^ (1 << i))]

def four_cycles(n):
    out = []
    rest_all = list(range(n))
    for i, j in itertools.combinations(range(n), 2):
        rest = [k for k in rest_all if k != i and k != j]
        for assign in itertools.product([0, 1], repeat=len(rest)):
            base = 0
            for k, b in zip(rest, assign):
                base |= b << k
            v00 = base; v10 = base | (1 << i); v01 = base | (1 << j); v11 = base | (1 << i) | (1 << j)
            out.append(frozenset([(min(a, b), max(a, b)) for a, b in
                                  [(v00, v10), (v00, v01), (v11, v10), (v11, v01)]]))
    return list(set(out))

def self_test_q3():
    n = 3
    E = hcube_edges(n)
    Eidx = {e: k for k, e in enumerate(E)}
    cycles = four_cycles(n)
    cyc_masks = []
    for c in cycles:
        mask = 0
        for e in c:
            mask |= 1 << Eidx[e]
        cyc_masks.append(mask)
    best = -1; bestset = None
    for s in range(1 << len(E)):
        ok = True
        for cm in cyc_masks:
            if s & cm == cm:
                ok = False; break
        if ok:
            c = popcount(s)
            if c > best:
                best = c; bestset = s
    print("Q3 brute-force ex(Q3,C4) =", best, "(expected 9)")
    kept = [E[k] for k in range(len(E)) if bestset >> k & 1]
    with open("_selftest_q3.txt", "w") as f:
        for u, v in kept:
            f.write(f"{min(u,v)} {max(u,v)}\n")
    sys.path.insert(0, ".")
    import verify_q7 as V
    cnt, msg = V.verify(V.load("_selftest_q3.txt"), 3)
    print("Q3 verifier:", msg, "| count", cnt, "(expected 9)")
    assert best == 9 and cnt == 9, "Q3 self-test FAILED"
    return True

# ---------- A276661 ----------
def self_test_a11():
    sys.path.insert(0, ".")
    import verify_a11 as V
    cg = [285, 433, 510, 550, 570, 581, 587, 590, 592, 593, 594]
    ok, msg = V.verify(cg)
    print("A11 CG-set:", msg)
    assert ok, "CG set must be dissociated"
    bad = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]  # fibonacci: 1+2=3 collision
    ok2, msg2 = V.verify(bad)
    print("A11 fib-set (expected fail):", msg2)
    assert not ok2, "corrupted set must fail"
    return True

# ---------- PG(2,5) ----------
def pg25_lines():
    # points = 1-dim subspaces of F_5^3 (normalized first nonzero coord = 1)
    pts = []
    for v in itertools.product(range(5), repeat=3):
        if v == (0, 0, 0):
            continue
        # normalize: first nonzero = 1
        for c in v:
            if c != 0:
                inv = pow(c, -1, 5)
                nv = tuple((x * inv) % 5 for x in v)
                break
        if nv not in pts:
            pts.append(nv)
    assert len(pts) == 31, len(pts)
    pidx = {p: i for i, p in enumerate(pts)}
    lines = []
    for a in range(5):
        for b in range(5):
            for c in range(5):
                if (a, b, c) == (0, 0, 0):
                    continue
                L = [(a * x + b * y + c * z) % 5 for x, y, z in pts]
                pts_on = [pidx[p] for p, val in zip(pts, L) if val == 0]
                if len(pts_on) == 6:
                    fs = frozenset(pts_on)
                    if fs not in lines:
                        lines.append(fs)
    assert len(lines) == 31, len(lines)
    return lines

def self_test_q6():
    sys.path.insert(0, ".")
    import verify_q6 as V
    lines = pg25_lines()
    edges = [sorted(L) for L in lines]
    ok, msg = V.verify(edges)
    print("PG(2,5) 31 lines:", msg)
    assert ok, "PG(2,5) lines must have tau=6"
    # a deliberately broken family: two disjoint 6-sets -> intersect fails
    bad = [[0,1,2,3,4,5],[6,7,8,9,10,11]] + [[0,6,12,13,14,15]]*0
    ok2, msg2 = V.verify(bad)
    print("broken family (expected fail):", msg2)
    assert not ok2
    return True

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    self_test_q3()
    self_test_a11()
    self_test_q6()
    print("ALL SELF-TESTS PASSED")
