# ex(Q9, C4) ≥ 1532

An explicit subgraph of the 9-dimensional hypercube `Q9` with **1532 edges and no 4-cycle**,
i.e.

```
ex(Q9, C4) ≥ 1532.
```

This improves the previous public explicit lower bound **1531**
([Erdős Problem a Day, 2026-08-11](https://erdosproblemaday.com/day/86-hypercube-q9-1531),
whose write-up states that bounded attempts to extend the graph to 1532 were unsuccessful).
It is a *lower bound only*: no optimality is claimed, and the asymptotic Erdős #86 question
is untouched.

The witness is certified three independent ways in Python and, additionally, by a
self-contained **Lean 4** proof (no Mathlib):

```
$ lean lean/Q9Witness.lean
"Q9 witness checked: ex(Q9, C4) >= 1532"
exit code: 0
```

## The witness

`edges_q9_1532.txt` — 1532 lines, one edge per line as `u v` with
`0 ≤ u < v < 512` and Hamming distance exactly 1.
SHA-256: `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`.

A **second, different** 1532-edge solution is included: `q9b_spin_6.txt`
(it shares only 516 of the 1532 edges with the first one, and passes the same checks).

## Verify (pure Python, no dependencies)

```bash
# 1) enumerate every one of the 4608 square faces of Q9 (C(9,2) * 2^7)
python verifiers/verify_c4_cycles.py edges_q9_1532.txt --n 9
#    -> VERIFIED n=9 kept=1532 cycles=4608

# 2) equivalent common-neighbour criterion (independent implementation)
python verifiers/verify_c4_common_neighbours.py edges_q9_1532.txt --n 9
#    -> VERIFIED (common-neighbour criterion)

# 3) red-team verifier written by a different team member
python verifiers/redteam_audit_verify.py c4_9 edges_q9_1532.txt
#    -> RESULT: PASS (C4-free)

# optional: self-tests of the verifiers on known-answer instances (Q3 has ex = 9)
cd verifiers && python selftest.py
```

Negative controls (the checks are not vacuous): deleting/additions of a completing edge,
duplicate edges, or non-edges are all rejected by these verifiers; the Lean file below is
likewise rejected when a single edge that closes a square is added (see `lean/CHECK.log`).

## Lean 4 certificate

`lean/Q9Witness.lean` is self-contained (only `import Init`) and proves, by closed
computation (`native_decide`):

* the listed pairs are 1532 distinct genuine edges of Q9;
* `c4free = true`: none of the 4608 square faces is fully present;
* every listed edge is a "satisfied" edge of the fully frustrated coupling
  `J(x,d) = (-1)^(popcount of the low d bits of x)`, and there are exactly 1532 such edges
  for the included 512-spin configuration;
* the fully frustrated identity: the product of the four couplings around every square is
  `-1` (which explains algebraically why no square can be complete);
* the bundled theorem `ex_Q9_C4_at_least_1532`.

`lean/CHECK.log` records the exact run with Lean 4.35.0 and the negative control
(adding the non-edge `(0,8)`, which closes 6 squares, makes Lean reject the file).

## How it was found

Canonical fully frustrated Ising coupling on Q9: `J(x,d) = (-1)^(popcount of the low d bits
of x)`.  The product of the four couplings around every square of Q9 is `-1`, so for any
spin configuration `s : {0,1}^9 -> {±1}` the set of satisfied edges
`{xy : s_x s_y = J(x,y)}` is automatically C4-free (a complete square would force
`1 = -1`).

We ran simulated annealing over the 512 spins maximizing the number of positive edges
(18 independent runs, ~5·10^8 single-spin flips each; runs reached 1526–1532, the best
value 1532 found twice), then reconstructed the spin configuration exactly from the edge
list.  Eighteen further tabu searches on edge sets seeded with the 1532-edge solution
(5.5·10^6 iterations each) never exceeded 1532, so 1532 is at least a strong local optimum.

This "odd-square / fully frustrated" construction is not new in itself: the values for
`n ≤ 7` go back to Derrida–Pomeau–Toulouse–Vannimenus (1979) and the `n = 8` attainment was
reported by Marinari–Parisi–Ritort (1995) (see arXiv:2603.29127 v5).  We are not aware of a
public `n = 9` value any larger than 1531 before this witness; the usual caveat applies
that private or unindexed work cannot be excluded.

## Scope and honesty

* **This is a lower bound.** `1532 ≤ ex(Q9,C4)`; no optimality and no asymptotic bound.
* Novelty comparison is against public, web-indexed sources (OEIS A245762, arXiv, the
  Erdős Problem a Day tracker) as of **2026-10-17**.  No larger public Q9 bound was found.
* Same-session negative results (a 305-edge witness for Q7, a(11) < 594 for OEIS A276661)
  are documented in `notes/` — they did **not** succeed and are included for transparency.

## Files

| path | content |
| --- | --- |
| `edges_q9_1532.txt` | the witness: 1532 Q9 edges, C4-free |
| `q9b_spin_6.txt` | second, different 1532-edge solution |
| `spins_q9.txt` | 512-bit spin configuration generating the witness |
| `RESULTS.md` | detailed write-up: record comparison, verification, structure |
| `verifiers/` | independent Python verifiers + self-tests |
| `lean/Q9Witness.lean` | Lean 4 certificate (self-contained) |
| `lean/CHECK.log` | Lean run transcript + negative control |
| `notes/REPORT_zh.md` | full session report (Chinese) |
| `notes/` | negative results on other problems (Q7/Q8, A276661) |

## Citation

```bibtex
@misc{exq9c4_1532,
  title  = {An explicit 1532-edge C4-free subgraph of the 9-dimensional hypercube},
  author = {Bil812 and AI research agents},
  year   = {2026},
  note   = {ex(Q9,C4) >= 1532; Python verifiers and a Lean 4 certificate},
  url    = {https://github.com/Bil812/erdos86-q9-c4}
}
```

## License

MIT — see `LICENSE`.
