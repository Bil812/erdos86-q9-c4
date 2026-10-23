# Erdős Problem a Day — submission text (Q9, f(9) ≥ 1532)

> **Status:** submitted 2026-10-18; independently verified **VERIFIED (as a certificate)**
> on 2026-10-24.  The review corrected the priority context: the value 1,532 was reported
> by Marinari–Parisi–Ritort (cond-mat/9410089, 1994) without a configuration, so this is an
> explicit certificate at that value, not a new number.  The text below is kept as submitted,
> with this correction noted; the repository README is the authoritative current version
> (tag `v1.1`).

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

**Relation to prior work (corrected 2026-10-24).**  The value 1,532 was reported by
Marinari–Parisi–Ritort (cond-mat/9410089, 1994) as an annealing result for D = 9, without a
published configuration.  The best *explicit certificates* we could find were 1,505 (GitHub,
May 2026) and 1,531 (the 2026-08-11 write-up on this site).  OEIS A245762 has no `a(9)`.
So this submission is an explicit certificate at the 1994 value — **not a new number and not
a new lower bound for the literature**; no priority is claimed.

**Scope:** does not determine `f(9)`, does not prove optimality, does not address the
asymptotic question.  The construction is an odd-square / fully frustrated Ising set.

**Provenance / AI disclosure:** this work was produced by **AI agents** (DeepSeek Harness,
`deepseek-flash`) operated from the account `Bil812`; the human account owner only initiated
the task, approved the direction, and authorised publication. The human did not do the
mathematics and did not run or check the verifiers. AI errors are possible, and independent
reproduction is welcome.
