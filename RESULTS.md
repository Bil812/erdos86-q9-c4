# f(9) ≥ 1532 — explicit C₄-free subgraph of Q₉ (lower bound only, 2026-10-18)

## Claim

There is an explicit subgraph of the 9-dimensional hypercube Q9 on 2^9 = 512 vertices
with **1532 edges and no 4-cycle**.  Hence

    ex(Q9, C4) ≥ 1532.

**Witness file:** `edges_q9_1532.txt` (1532 lines, `u v`, `0 ≤ u < v < 512`,
Hamming distance exactly 1, no 4-cycle among the 4608 square faces of Q9).
SHA-256: `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`.

A **second, different** 1532-edge solution exists: `q9b_spin_6.txt`
(differs from the first in 1016 edges, same verification).

## Relation to prior public work (as of 2026-10-18)

The best public Q₉ lower bound we could find was **1531** (unreviewed, AI-assisted):
* "Erdős #86: a 1,531-edge C4-free subgraph of Q9", Erdős Problem a Day, 2026-08-11,
  <https://erdosproblemaday.com/day/86-hypercube-q9-1531> (with an audited 1,506-edge
  predecessor and an identified external 1,505-edge certificate; the page states that
  bounded attempts to extend to 1532 were unsuccessful).
* The #86 attempts page (<https://erdosproblemaday.com/problem/86>) showed no later
  entry when audited on 2026-10-17.
* OEIS A245762 has no Q9 term (last edit 2026-09-02); Minamoto et al. (arXiv:2603.29127
  v5) cover Q6–Q8 only (their DPTV table stops at n = 8).

Scope caveat: this is a *public / web-indexed* comparison. The odd-square construction
goes back to the statistical-physics literature (Derrida–Pomeau–Toulouse–Vannimenus 1979
for D ≤ 7; Marinari–Parisi–Ritort 1995 for D = 8 per arXiv:2603.29127 v5); no n = 9
value was found there in our audit, but unindexed private/old work cannot be excluded.
This is a **lower bound only** — no optimality is claimed.

## How the witness was found

Canonical fully frustrated Ising coupling on Q9:

    J(x, d) = (-1)^(popcount of the low d bits of x),   d = 0..8,

has the property that the product of the four couplings around every square of Q9 is −1.
Therefore, for **any** spin configuration s : {0,1}^9 → {±1}, the set of "satisfied"
("positive") edges {xy : s_x s_y = J(x,y)} is automatically C4-free: if a square were
complete, multiplying the four satisfied-edge equations gives 1 = (product of the four
couplings) = −1, a contradiction.

We ran simulated annealing over the 512 spins maximizing the number of positive edges
(`spinmax.c`, 18 independent runs, ~5·10^8 single-spin flips per run; runs reached
1526–1532, best 1532, found twice).  18 further tabu searches on edge sets seeded with
the 1532-edge solution (`hitter.c`, 5.5·10^6 iterations each) never exceeded 1532, so
1532 is at least a strong local optimum.

The spin configuration of the witness was reconstructed exactly from the edge list
(BFS over satisfied edges; `spins_q9.txt`, zero inconsistencies, positive-edge set equals
the witness set).  This is what makes the Lean formalization a short algebraic argument
rather than a giant enumeration.

## Verification (three independent checks)

1. **Lead's cycle enumeration** (`research/common/verify_q7.py --n 9`):
   enumerates all C(9,2)·2^7 = 4608 square faces (in fact the deduplicated cycle set),
   all 1532 lines are valid Q9 edges, none of the 4608 faces is fully present:
   `VERIFIED n=9 kept=1532 cycles=4608`.
2. **Lead's common-neighbour criterion** (`research/common/verify_c4_alt.py`):
   a graph is C4-free iff every vertex pair has at most one common neighbour; checked
   over all 9216 Hamming-distance-2 pairs: `pairs_with_>=2_common_neighbours=0`.
3. **Red-team, independent implementation** (`research/q6/audit_verify.py c4_9 <file>`,
   written by teammate `q6-hypergraph`, not the finder): PASS — 1532 distinct valid
   edges, 4608 faces enumerated, 0 present, independent common-neighbour check 0.
   The second solution `q9b_spin_6.txt` PASSes as well.  Negative controls (a file with
   one complete square, a file with a duplicate edge) are correctly rejected, so the
   verifier is not vacuous.

Structural data of the witness: degrees {5:14, 6:494, 7:2, 8:2}, degree sum 3064,
all 512 vertices used; direction counts 168/170/170/170/174/170/170/170/170;
every one of the 4608 squares has exactly 1 or 3 present edges
(histogram {1:784, 3:3824}) — i.e. a genuine odd-square / fully frustrated set.

## Lean formalization — VERIFIED

`research/lean/Q9Witness.lean` (self-contained, no Mathlib) contains the edge list, the
spin configuration, and proves by `native_decide`:

* `edges.length = 1532` and every listed pair is a genuine Q9 edge;
* `c4free = true` (direct finite check over all 4608 squares);
* every listed edge is a positive edge of the coupling;
* the number of positive edges for these spins is exactly 1532;
* the fully frustrated identity: the four-coupling product around every square is −1;
* `ex_Q9_C4_at_least_1532` bundling the above.

**Checked with Lean 4.35.0 (Windows) on 2026-10-18.** The proof uses `native_decide` (trusted native evaluation), not a pure kernel reduction; `#print axioms` shows the `native_decide` evaluation axioms — see `lean/AXIOMS.log`. There is no `sorry`/`admit` and no hand-written `axiom`.

```
$ lean Q9Witness.lean
"Q9 witness checked: ex(Q9, C4) >= 1532"
exit code: 0   (5.1 s)
```

**Negative control (the check is not vacuous):** appending the non-edge `(0,8)`
(which closes 6 squares of the witness) makes Lean reject the file:
`native_decide` reports `c4free = true` is false (exit code 1).
Full transcript: `research/lean/CHECK.log`.  Generator: `research/common/gen_lean_q9_v2.py`.
Toolchain used locally at `D:\lean-work\lean3\lean-4.35.0-windows\bin\lean.exe`.

## Files

| file | content |
| --- | --- |
| `edges_q9_1532.txt` | witness: 1532 Q9 edges, C4-free (canonical file) |
| `q9b_spin_6.txt` | second, different 1532-edge solution |
| `spins_q9.txt` | 512-bit spin configuration generating the witness |
| `q9_spin_3.txt` | raw SA output that produced the 1532 witness |
| `spinmax.c` | spin-glass SA (`spinmax 9 seed seconds outfile`) |
| `hitter.c` | edge-set tabu search (`hitter 9 W seed seconds outfile seedids`) |
| `edges_q9_1532_ids.txt` | witness as edge ids for `hitter.c` |
| `research/common/verify_q7.py` | cycle-enumeration verifier (works for any n) |
| `research/common/verify_c4_alt.py` | common-neighbour verifier |
| `research/lean/Q9Witness.lean` | Lean 4 certificate |
