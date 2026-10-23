# f(9) ≥ 1532 — an explicit certificate at the 1994 Marinari–Parisi–Ritort value

## Claim

There is an explicit subgraph of the 9-dimensional hypercube Q9 on 2^9 = 512 vertices with
**1532 edges and no 4-cycle**.  Hence

    ex(Q9, C4) ≥ 1532.

**The number 1532 is not new**: it was *reported* by Marinari, Parisi and Ritort
(cond-mat/9410089, 1994) as an annealing result for the fully frustrated hypercubic model at
D = 9 (energy per spin −0.4947916…, i.e. 1,532 satisfied bonds of 2,304), **without a
published configuration**.  This repository contributes an explicit, reproducible
certificate at that value (and a Lean 4 check), not a new lower bound.

**Witness file:** `edges_q9_1532.txt` (1532 lines, `u v`, `0 ≤ u < v < 512`,
Hamming distance exactly 1, no 4-cycle among the 4608 square faces of Q9).
SHA-256: `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`.

A **second, different** 1532-edge solution exists: `q9b_spin_6.txt` (shares 1,024 edges with
the first; same verification).

## Independent verification (2026-10-24)

Erdős Problem a Day checked the certificate with their own code (none of ours was run) and
replied **VERIFIED — as a certificate**: both graphs have 1,532 edges and no 4-cycle (two
instruments: face enumeration and adjacency-matrix codegrees); faces carry 1 or 3 edges
(784 and 3,824); the two graphs share 1,024 edges; under the MPR coupling the spin state in
`spins_q9.txt` gives exactly 1,532 satisfied bonds with energy per spin −95/192 =
−0.4947916…, matching the 1994 printed value to every digit.  They also corrected the
priority context (MPR 1994) and their own 1,531 page.  They did **not** check the Lean file.
Full excerpt: `REVIEW_2026-10-24.md`.

## Relation to prior work (as of 2026-10-24)

| Source | Q₉ lower bound | date | note |
|---|---|---|---|
| Marinari–Parisi–Ritort, cond-mat/9410089 | **1532** (reported) | 1994 | annealing value, energy per spin −0.4947916…; no configuration published |
| "Erdős #86: a 1,531-edge C4-free subgraph of Q9", Erdős Problem a Day | 1531 | 2026-08-11 | explicit certificate; its 1,532 attempts had failed; page since corrected |
| GitHub `rafalwronapl/erdos86-hypercube-c4` | 1505 | 2026-05 | explicit certificate |
| OEIS A245762 | no a(9) term | last edit 2026-09-02 | data only a(1..6); comments up to a(8) |
| **this repository** | **1532** (explicit) | 2026-10-18 | explicit certificate + Lean at the MPR-1994 value; independently verified 2026-10-24 |

Scope caveat: this is a *public / web-indexed* comparison; the 1994 value is from the
statistical-physics literature (no configuration published there).  This is a **lower bound
only** — no optimality is claimed.

## Where it sits

* General window at n = 9: **1532 ≤ ex(Q9,C4) ≤ 1584** (upper bound by subcube averaging
  ex(Qₙ) ≤ 2n/(n−1)·ex(Qₙ₋₁) with the published ex(Q7,C4) ≤ 308: 704 then 1584).
* **Odd-square family:** odd-square edge sets in Q9 cannot exceed **1,536** (field bound: all
  degrees would be 6); MPR did not reach it; whether 1,536 is attained is open (Minamoto,
  arXiv:2603.29127 v5, Open Problem 7).
* Our search (18 spin-annealing runs + 18 seeded tabu searches) plateaued at 1,532, matching
  the 1994 annealing result; we make no claim about 1,533–1,536.

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
1532 is at least a strong local optimum — consistent with the 1994 annealing value.

The spin configuration of the witness was reconstructed exactly from the edge list
(BFS over satisfied edges; `spins_q9.txt`, zero inconsistencies, positive-edge set equals
the witness set).  This is what makes the Lean formalization a short algebraic argument
rather than a giant enumeration.

## Verification (three independent Python checks + Lean)

1. **Cycle enumeration** (`verifiers/verify_c4_cycles.py --n 9`): all 4,608 square faces
   enumerated; 0 complete: `VERIFIED n=9 kept=1532 cycles=4608`.
2. **Common-neighbour criterion** (`verifiers/verify_c4_common_neighbours.py`): 0 pairs at
   Hamming distance 2 with ≥ 2 common neighbours: `VERIFIED`.
3. **Red-team verifier** (`verifiers/redteam_audit_verify.py c4_9`): `RESULT: PASS`.
4. **Lean 4.35.0** (`lean --run` not needed; plain `lean Q9Witness.lean`): exit code 0,
   proves `Q9.ex_Q9_C4_at_least_1532`.  The proof uses `native_decide`; the evaluation
   axioms are disclosed in `lean/AXIOMS.log`.  A negative control (adding a square-closing
   non-edge) is rejected.

## Structure of the witness

Every one of the 4,608 faces carries exactly 1 or 3 edges (784 faces with 1 edge, 3,824 with
3): the odd-square / fully frustrated signature.  Degree sequence {5:14, 6:494, 7:2, 8:2};
all 512 vertices used; per-direction edge counts 168/170/170/170/174/170/170/170/170.

## Files

| file | content |
| --- | --- |
| `edges_q9_1532.txt` | certificate: 1532 Q9 edges, C4-free |
| `q9b_spin_6.txt` | second 1532-edge solution |
| `spins_q9.txt` | 512-bit spin configuration |
| `q9_spin_3.txt` | raw SA output that produced the certificate |
| `lean/Q9Witness.lean` | Lean 4 certificate |
| `lean/CHECK.log`, `lean/AXIOMS.log` | Lean transcript, axiom output |
| `REVIEW_2026-10-24.md` | independent verification verdict |
