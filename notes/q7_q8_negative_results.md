# ex(Q7,C4) and ex(Q8,C4) 閳?results (teammate c4-hypercube)

## Status summary

| target | known record | this session | verified? |
| --- | --- | --- | --- |
| ex(Q8,C4) >= 682 | 680 (OEIS A245762, Aug 2026, stale) / **682 already published** (arXiv:2603.29127 current version, g(8)=682) | independent reproduction of a **682-edge** C4-free subgraph of Q8 | **yes**, from scratch (`edges_q8.txt`, 0 of 1792 squares present) |
| ex(Q7,C4) >= 305 | open (304 <= ex <= 308) | **not found**; exhaustive negatives show all 8 independent 304-edge solutions we generated are 2-for-1, 3-for-2 and 4-for-3 swap-locally maximal | n/a (negative results) |

**Novelty correction (from Lead's check of arXiv:2603.29127 current version):** the value
682 is the published odd-square value g(8)=682, so our 682 witness is an *independent
reproduction*, **not** a new record, and must not be reported as one. The only open target
in this family is a **non-odd-square** 305-edge C4-free subgraph of Q7; we did not find one
and make no claim beyond the exhaustive small-swap negatives below.

## Q8: verified 682-edge C4-free subgraph (independent reproduction)

`edges_q8.txt` (682 lines, `u v`, `0 <= u < v < 256`). Fresh-process verification:

```
workdir: research/c4-hypercube
python verify_q8.py edges_q8.txt 8
```

```
n = 8, admissible edges read = 682 (all genuine, no duplicates)
4-cycles enumerated = 1792 (expected 1792)
4-cycles fully present = 0
ex(Q8,C4) >= 682
VERIFIED 8
```

Cross-check with the Lead's verifier:
`python research/common/verify_q7.py research/c4-hypercube/edges_q8.txt --n 8`
-> `VERIFIED n=8 kept=682 cycles=1792`.

Construction: canonical fully frustrated coupling on Q8,
`J(x,dim) = (-1)^popcount(x & ((1<<dim)-1))`; every square has coupling product -1, so the
positive edges (`s_x s_y = J`) of any 256-spin configuration form an odd-square, hence
C4-free, edge set. `gen_from_spins.py` re-derives the 682 edges from the 256-bit spin
string and re-verifies (reproduces the advertised degree histogram `{4:2, 5:168, 6:86}` and
square-positive histogram `{1:301, 3:1491}`). The spin vector is the one in the public
Minamoto repository's `ODDSQUARE_BRIDGE` package; the independent verification and edge
list here are this session's contribution.

Evidence that 682 is the maximum of this (odd-square) family: 12 independent simulated
annealing runs over the 256 spins (`spinmax.c`, ~2.3e9 single-spin flips, 6 restarts each)
all stopped at exactly 682 and never exceeded it. (Not a proof; and non-odd-square
C4-free subgraphs are not covered by this family.)

## Q7: no 305 found; exhaustive small-swap negatives

Record stays 304 <= ex(Q7,C4) <= 308; no improvement and no optimality proof here.

### (1) Odd-square family maximum on Q7 is exactly 304

`spinmax.c` = simulated annealing over the 128 spins of the fully frustrated coupling,
maximising positive edges. 8 independent runs (different seeds, 6 restarts, ~1.2e8
flips/run): **all 8 reached exactly 304 and never more**. This agrees with the published
g(7)=304. Each run's best edge set is stored (`q7_spin_1.txt` ... `q7_spin_8.txt`,
304 edges, C4-free, verified by `verify_q8.py` used with n=7: `VERIFIED 7`).

Pipeline sanity check: the same `spinmax.c` on Q6 reaches exactly **132** = ex(Q6,C4)
(known exact), so the search/verification pipeline is sound.

### (2) Exhaustive 2-for-1 exchange: no 305 reachable by dropping one kept edge, adding two removed edges

`exchange.c` (exhaustive, exact incremental counts): for each kept edge `k'` and each pair
`r1,r2` of the 144 removed edges, check whether `K - {k'} + {r1,r2}` is C4-free. Result for
**all 8** independent 304-edge solutions:

```
NO 2-for-1 exchange exists  (all 304 choices of k' and all removed-edge pairs)
```

This is an exhaustive negative *within that neighbourhood*: no 305-edge set at swap
distance (1 kept out, 2 in) from any of the 8 solutions. It is not a global statement.

### (3) Exhaustive 3-for-2 exchange: also none

`exchange32.c` (exhaustive over all `C(304,2)=46056` kept-edge pairs and all triples of
removed edges, with exact feasibility pruning): for all 8 solutions,

```
NO 3-for-2 exchange: 46056 kept-pairs checked, 0 candidate triples feasible
```

### (4) Exhaustive 4-for-3 exchange: also none (and a stronger statement)

`exchange43.c` (exhaustive over all `C(304,3) = 4,636,304` kept-edge triples and all
candidate quartets of removed edges, exact pruning): for all 8 solutions,

```
NO 4-for-3 exchange: 4636304 kept-triples checked, 0 quartets, max #candidates=2
```

Stronger: after deleting any 1 / 2 / 3 kept edges, at most **1 / 2 / 2** removed edges are
individually addable respectively (the 4-for-3 run reports `max #candidates = 2` over all
4,636,304 triples; the 2-for-1 and 3-for-2 runs find no feasible candidate pair/triple).
Since adding 4 removed edges requires
4 individually addable ones, no (`k` kept out, `k+1` removed in) exchange to 305 exists
for k = 1, 2, 3 from any of the eight independent 304-edge odd-square solutions.

### (5) Frontier / novelty audit (read this before citing anything here)

* OEIS A245762 (comment 2026-08-27) still says `a(8) >= 680`; that entry is **stale**:
  arXiv:2603.29127 v5 (2026-08-28) proves `g(8) = 682`, where `g(n)` is the maximum size
  of an odd-square edge set (positive edges of a fully frustrated coupling). Hence 682
  was already published 閳?our `edges_q8.txt` is an **independent reproduction, not a new
  record**, and must not be reported as one.
* `g(7) = 304` is only the **odd-square optimum**. General C4-free subgraphs of Q7 may
  contain squares with 0 or 2 selected edges, so `ex(Q7,C4) >= 305` is **not excluded**
  and remains open. Our exhaustive 2-for-1 / 3-for-2 / 4-for-3 negatives apply only to
  the odd-square 304 solutions we generated (8 of them), not to all 304-edge graphs and
  not to large neighbourhoods.
* Upper bounds are unchanged: `ex(Q7,C4) <= 308` (subcube averaging,
  `floor(2*7*132/6)`) and `ex(Q8,C4) <= 704` (`floor(2*8*680/7)`); both survive the
  improved lower bound for Q8.
* Net: this session contributes (i) an independently verified 682-edge Q8 witness and
  (ii) rigorous local-exclusion negatives for 305 on Q7; **no new record**.

### (6) Why the odd-square 304 solutions are hard to leave (structural observation)

In an odd-square 304 solution every square has 1 or 3 kept edges; exactly 576 squares have
3 kept edges and 96 have 1 (since 304*6 = 1824 = 3*576 + 96). A square with 3 kept edges
contains exactly **one removed edge**, so each of the 144 removed edges has on average
576/144 = **4 "critical" squares** that must first be broken (one of their 3 kept edges
removed) before that edge can ever be added. One kept-edge deletion touches only its 6
squares, which is why `nc` (individually addable removed edges) stays <= 1 after one
deletion and < 3 after two deletions 閳?the exhaustive computations above confirm this
quantitatively. Escaping to 305 therefore needs a coordinated multi-edge move; the cost
function is very flat around these solutions.

### (7) Tabu search on edge sets

`hitter.c` = tabu search over edge toggles with cost `W*(#4-cycles) + #removed`, seeded
with the verified 304-edge solution (`q7_spin_1.txt`), 12 independent processes, W in
{1,2,3,5}, 470 s each. **No solution with more than 304 kept edges was found** (logs
`q7_t_*.log`). (An earlier batch used a truncated seed of 257 edges because of a
seed-passing bug; those runs are not evidence either way and were discarded.)

No CP-SAT/HiGHS run was made by this teammate for Q7 exactness because the Lead ran the
exact MIP / HiGHS lane concurrently.

## Honest bottom line

* Q8: 682 witness independently verified (matches the published odd-square value; OEIS
  A245762 is stale at 680). No new record claim.
* Q7: **no improvement, no optimality proof**. The 305 lower bound remains open. Our
  contribution is a set of exhaustive local-exclusion results: from eight independent
  304-edge odd-square solutions, none admits a (`k-1` in, `k` out) improvement for
  k = 1, 2, 3, i.e. 305 is not one-to-three-swap reachable from any of them, and the family
  maximum under the fully frustrated coupling is exactly 304.

## Files

| file | meaning |
| --- | --- |
| `edges_q8.txt` | verified witness: 682 kept edges of Q8, no 4-cycle |
| `verify_q8.py` | independent from-scratch verifier (`python verify_q8.py edges_q8.txt 8`) |
| `gen_from_spins.py` | regenerates the 682-edge set from the 256-spin vector and re-verifies |
| `spinmax.c` | spin-glass SA over fully frustrated coupling (Q6 -> 132, Q7 -> 304, Q8 -> 682) |
| `hitter.c` | tabu search over edge sets, optional seed file ("u v" or edge ids) |
| `exchange.c` | exhaustive 2-for-1 exchange test |
| `exchange32.c` | exhaustive 3-for-2 exchange test |
| `exchange43.c` | exhaustive 4-for-3 exchange test |
| `two_copy.py` | layer-doubling construction + Hopcroft閳ユ彅arp / K鏋歯ig min vertex cover |
| `edges_to_ids.py` | helper (edge list -> edge ids) |
| `q7_spin_1.txt` ... | eight independent 304-edge C4-free Q7 solutions |
| `q7_t_*.log`, `q7_spin_*.log` | raw search logs |

## Effort

~55 min wall clock, 20 logical cores; roughly 60 CPU-min spin annealing (Q7+Q8) and
~60 CPU-min tabu search, plus seconds for the exhaustive exchange tests.


