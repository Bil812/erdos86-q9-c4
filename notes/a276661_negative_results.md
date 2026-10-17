# Target B — a(11) for OEIS A276661 (Erdős distinct subset sums)

**Status: NO NEW RECORD FOUND. a(11) ≤ 594 (Conway–Guy) remains the best value we can certify.**
No 11-element set `S ⊆ {1,...,593}` with pairwise distinct subset sums was found. Everything
below is stated exactly as run; nothing is claimed beyond what was verified.

- Witness file `witness_a11.json` = the **baseline** Conway–Guy set (max 594, `"record": false`).
  It is *not* a new record; it is included so the verifier and the checking pipeline are exercised.
- Verifier: `verify_a11.py` (loads the JSON, recomputes all 2^11 subset sums from scratch, checks
  |set| = 11, positivity, distinctness, an independent full 3^11 signed-relation scan, and the max).

## Verification command and output (fresh process)

```
> python verify_a11.py witness_a11.json
|S| = 11, all elements positive & distinct
subset sums: 2048 / 2048 pairwise distinct  (range 0..5885)
signed relations: 0 nontrivial {-1,0,1} relations (independent check)
max element M = 594
NOT a new record: M = 594 >= 594 (known Conway-Guy bound; this is a baseline check)
VERIFIED
EXIT=0
```

The independent checker `research/common/verify_a11.py` was also pointed at the same file by the Lead
and accepts it.

## What was tried (all failed to produce M < 594)

Definitions: a set is *dissociated* iff all 2^11 subset sums are distinct iff no nontrivial
`ε ∈ {-1,0,1}^11` has `Σ ε_i v_i = 0`. For a candidate 11-set `v`, `cost(v)` = number of unordered
pairs of distinct subsets with equal sum (0 ⇔ dissociated).

1. **Clamping the Conway–Guy construction.** Taking the known CG set
   `[285,433,510,550,570,581,587,590,592,593,594]` and shifting its top `k` elements down by 1 gives
   9 sets with max **593**; their costs are 8, 16, 20, 25, 49, 50, 51, 129, 146. The best one,
   `[285,432,509,549,569,580,586,589,591,592,593]`, has cost 8 coming from the *single* relation
   `285+589+592+593 = 432+509+549+569`. So a max-593 witness is exactly **one relation** away from
   these seeds.
2. **Exhaustive 1-element repair.** From all 9 max-593 seeds, every position × every replacement
   value in 1..593 (6523 candidates per seed): **no cost-0 set**. (lab3.py)
3. **Exhaustive 2-element repair** (C, `search.c` mode 0): all pairs of positions, new values within
   ±30 (and spot checks at larger ranges) around all 9 seeds — 214,992 candidates — **no cost-0 set**.
4. **Simulated annealing in set space** (`search.c` mode 1, 300k–2M iterations, several seeds):
   never went below cost 8; the cost-1 seeds are a strong local optimum.
5. **Popov-style "free maximum" reformulation** (the main new idea). Any 11-set with maximum M is
   `V = {M − W_0, ..., M − W_10}` with `W_0 = 0 < W_1 < ... < W_10`; for fixed W the set of *admissible*
   maxima M is explicitly computable, so define `f(W)` = least admissible `M > W_10`. Then
   `a(11) = min_W f(W)`, and `f(W)` is a much smoother objective than "no subset-sum collisions".
   Results:
   - CG's W = `[0,1,2,4,7,13,24,44,84,161,309]` gives **f = 594** (the CG set itself).
   - Turning Popov's published n=12 W `[0,5,8,10,12,16,27,49,88,164,312,603]` into an 11-element W
     (delete its largest entry) gives f = **603**; other entries of the same W give f = 751..894.
     Popov's n=13 W with two entries deleted gives f ≥ 612; all n=12/13 single/double truncations
     are ≥ 603 — none reaches 593.
   - **Full exhaustive 1-opt in W-space** (every W_i, every value): f stays 594 (CG seed) / 603
     (Popov seed). No improvement.
   - **Exhaustive 2-opt in W-space** with |Δ| ≤ 40 and ≤ 100 on both seeds, all 55 coordinate pairs
     (`wsearch.c` mode 2): f stays 594 / 603. No improvement.
   - SA over W (`wsearch.c` mode 3): no improvement.
   - Important structural fact this exposed: for a random W the "E=0" signed relation
     `Σ ε_i W_i = 0, Σ ε_i ∈ {-1,0,1}` usually holds, making *every* M fail; CG's W is unusually
     "clean", which is why random starts are hopeless (see 6).
6. **Random-restart hill climbing over W** (`randsearch.c`, 10 parallel instances, 240 s each):
   best f over all random starts was **914** — far worse than 594. Random structures are not near
   the frontier; the CG construction is a deep local optimum.
7. **CP-SAT exact model** (`cpsat_alldiff.py`, OR-Tools 9.15, 8 workers, 300 s): 11 integer vars in
   [1,593], strictly increasing, 2048 subset-sum IntVars with `AddAllDifferent`, hint = the best
   max-593 near-miss seed. Result: **UNKNOWN** after 300 s (no feasible solution, no infeasibility
   proof). The equivalent 88573-sign-vector big-M formulation was not needed because this encoding
   is the stronger one.

## Honest assessment

* No witness with M < 594 was found; we cannot claim any improvement of a(11).
* The Conway–Guy set is a very strong local optimum: it is optimal under every exhaustive
  1-element and 2-element (±100) neighbourhood we could test, both in set space and in the
  "free-maximum" W space. The only max-593 sets close to it fail by exactly one signed relation.
* Since Popov's W for n=12,13 *is* a small perturbation of CG's W (each entry shifted up by 3–18,
  which lowers the max by 7 and 35 respectively), a max-593 set for n=11 would plausibly also be a
  perturbation of CG's W — but no such perturbation exists in the ±100 two-coordinate neighbourhood.
  Any improvement likely requires a genuinely different construction or a much larger search.
* Resources used: ~1.5 CPU-hours (≈20 core-min C heuristics, ≈40 core-min CP-SAT, remainder
  Python analysis), 20-core Windows box.

## Follow-up (bounded 20-min task): neighbouring OEIS terms a(12), a(13)

Same "free maximum" machinery (`wsearchN.c`, n = 12, 13), pointed at Popov's published sets.
The seeds reproduce Popov's values exactly:
- n=12: W12 = `[0,5,8,10,12,16,27,49,88,164,312,603]`, **f(W12) = 1157**, V = Popov's 12-set
  `{1157,1152,1149,1147,1145,1141,1130,1108,1069,993,845,554}`;
- n=13: W13 = `[0,6,9,12,19,24,29,52,95,171,318,612,1172]`, **f(W13) = 2249**, V = Popov's 13-set.

Exhaustive neighbourhoods searched (all completed, none improved):

| neighbourhood | n=12 (target f ≤ 1156) | n=13 (target f ≤ 2248) |
|---|---|---|
| full 1-opt (one W coordinate, every value) | 1,976 candidates, f stays **1157** | 3,742 candidates, f stays **2249** |
| 2-opt all coordinate pairs, abs(delta) ≤ 60 | 66 pairs × 121² = 966,306 grid points, f stays **1157** | 78 pairs × 121² = 1,141,938 grid points, f stays **2249** |
| 2-opt all pairs, abs(delta) ≤ 100 | 55 pairs × 201² = 2,222,055 grid points, f stays **1157** | not run (time-box) |
| 3-opt all coordinate triples, abs(delta) ≤ 4 | 165 triples × 9³ = 120,285 grid points, f stays **1157** | 220 triples × 9³ = 160,380 grid points, f stays **2249** |

Each grid point required recomputing the least admissible maximum f(W) (up to ~1,080 subset-sum
dissociatedness tests for n=13). **No W with f(W) < 1157 (resp. < 2249) was found**, so no
`witness_a12.json` / `witness_a13.json` was written — Popov's values 1157 and 2249 remain unchanged
in our hands. Verifier for these sizes is `verify_an.py` (recomputes 4096 / 8192 subset sums).
This is a negative result, not evidence of optimality: f is 1-opt/2-opt/3-opt locally optimal at
Popov's W's, so any +1 improvement requires a non-local move or a different construction.
Follow-up resources: ≈1.4 CPU-hours (23–24 parallel single-thread processes).

## Files

| file | purpose |
|---|---|
| `witness_a11.json` | baseline CG set, max **594**, explicitly not a record |
| `verify_a11.py` | independent 11-set verifier (all checks from scratch) |
| `verify_an.py` | independent verifier for n = 11, 12, 13 |
| `search.c` / `search.exe` | set-space 2-opt + SA search |
| `wsearch.c` / `wsearch.exe` | W-space ("free maximum") 1-opt/2-opt/SA search, n = 11 |
| `wsearchN.c` / `wsearchN.exe` | W-space search for n = 12, 13 (1-opt / 2-opt / 3-opt / SA) |
| `randsearch.c` / `randsearch.exe` | random-restart hill climbing in W space |
| `cpsat_alldiff.py` | OR-Tools CP-SAT model (2048 subset sums + AllDifferent) |
| `lab*.py` | exploratory scripts (clamped-CG seeds, hole scans, Popov truncations) |
| `w_*.txt`, `rs*.txt`, `r1*_*.txt`, `s12_*.txt`, `t1*_3opt.txt` | raw search logs |
