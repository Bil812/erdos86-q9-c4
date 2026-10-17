# Erdős Problem a Day — submission text (Q9, f(9) ≥ 1532)

Submit at <https://erdosproblemaday.com/submit> (problem #86).

---

**Problem:** Erdős #86 (hypercube C₄-free subgraphs). `f(n) = ex(Qₙ,C₄)`.

**Claim (lower bound only):** `f(9) ≥ 1532`.

**Certificate:** explicit edge list of 1532 edges on the 512 vertices of Q₉
(`0 ≤ u < v < 512`, Hamming distance exactly 1), all 4608 square faces checked:
none is complete.

- File: `edges_q9_1532.txt`
- SHA-256: `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`
- Repository: <https://github.com/Bil812/erdos86-q9-c4> (tag `v1.0`)

**Verification (dependency-free Python):**

```
python verifiers/verify_c4_cycles.py edges_q9_1532.txt --n 9
# -> VERIFIED n=9 kept=1532 cycles=4608
python verifiers/verify_c4_common_neighbours.py edges_q9_1532.txt --n 9
# -> VERIFIED (common-neighbour criterion)
python verifiers/redteam_audit_verify.py c4_9 edges_q9_1532.txt
# -> RESULT: PASS (C4-free)
```

**Lean 4:** `lean/Q9Witness.lean` (Lean 4.35.0, `native_decide`) compiles with exit code 0
and proves `Q9.ex_Q9_C4_at_least_1532`.  The `native_decide` evaluation axioms are disclosed
in `lean/AXIOMS.log`; a negative control (adding an edge that closes a square) is rejected.
There is no `sorry`/`admit` and no hand-written axiom.

**Relation to prior public work (as of 2026-10-18):** we found two public Q₉ lower bounds:
1505 (an explicit certificate on GitHub, May 2026) and 1531 (your 2026-08-11 write-up, whose
text states attempts to reach 1532 failed).  OEIS A245762 has no `a(9)`.  This submission is
**+1 over the best public claim we could find**; we make no priority claim and cannot exclude
unindexed work (in particular, old statistical-physics computations of fully frustrated Ising
ground states for D = 9).

**Scope:** does not determine `f(9)`, does not prove optimality, does not address the
asymptotic question.  The construction is an odd-square / fully frustrated Ising set.

**AI disclosure:** the computational search and the draft verifier/Lean scaffolding were
produced by AI agents under human direction; the human author selected the problem/method,
directed the search, independently re-verified the certificate (separate Python verifier and
Lean run), and wrote the verification record.
