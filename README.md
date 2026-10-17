# f(9) ≥ 1532 — a certifiable finite lower bound for Erdős #86

> **Claim (lower bound only).** We exhibit an explicit C₄-free subgraph of the 9-dimensional
> hypercube Q₉ with **1532 edges**, establishing the lower bound **f(9) ≥ 1532**, where
> f(n) = ex(Qₙ, C₄) is the maximum number of edges in a C₄-free subgraph of Qₙ.
>
> This is **not** a determination of f(9), **not** a proof of optimality, and **not** a
> resolution of the asymptotic Erdős #86 question. No priority is claimed.

## Witness

* Edge list: **`edges_q9_1532.txt`** — 1532 lines `u v` with `0 ≤ u < v < 512` and Hamming
  distance exactly 1; 1532 distinct edges.
* **SHA-256** of `edges_q9_1532.txt`:
  `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`.
  The repository stores all files byte-for-byte (`.gitattributes` sets `* -text`), so this
  hash refers to the exact bytes you get from GitHub; `MANIFEST.sha256` lists the hash of
  every file.
* The graph is the set of positive edges of a fully frustrated (odd-square) Ising
  configuration on Q₉: every one of the 4608 square faces of Q₉ has exactly 1 or 3 selected
  edges.  The 512-spin configuration is in `spins_q9.txt`.
* A **second, different** 1532-edge solution is included as `q9b_spin_6.txt` (it shares only
  516 edges with the first and passes the same checks).

## Verification

All commands are dependency-free Python 3 except the Lean check.

1. **Cycle enumeration** (all `C(9,2)·2⁷ = 4608` square faces):

   ```
   python verifiers/verify_c4_cycles.py edges_q9_1532.txt --n 9
   -> VERIFIED n=9 kept=1532 cycles=4608
   ```

2. **Common-neighbour criterion** (independent formulation: a graph is C₄-free iff every
   pair of vertices has at most one common neighbour):

   ```
   python verifiers/verify_c4_common_neighbours.py edges_q9_1532.txt --n 9
   -> VERIFIED (common-neighbour criterion)   [0 pairs with >=2 common neighbours]
   ```

3. **Red-team verifier** (written by a different team member, from the mathematical
   definition, not reusing the checkers above):

   ```
   python verifiers/redteam_audit_verify.py c4_9 edges_q9_1532.txt
   -> RESULT: PASS (C4-free)
   ```

4. **Lean 4** (Lean 4.35.0, x86_64-w64-windows-gnu, commit `eb6cafb7`), self-contained
   file `lean/Q9Witness.lean` (only `import Init`, no Mathlib):

   ```
   lean lean/Q9Witness.lean
   -> "Q9 witness checked: ex(Q9, C4) >= 1532"
      exit code 0
   ```

   The theorem is `Q9.ex_Q9_C4_at_least_1532 :
   edges.length = 1532 ∧ edges.all validEdge = true ∧ c4free = true`.

   **Trust caveat (disclosed on purpose):** the proof uses `native_decide`, i.e. trusted
   *native evaluation*, not a pure kernel reduction.  `#print axioms` shows the
   `native_decide` axioms, not only the three standard ones:

   ```
   'Q9.ex_Q9_C4_at_least_1532' depends on axioms:
     [Q9.edges_all_valid._native.native_decide.ax_1_1,
      Q9.edges_length._native.native_decide.ax_1_1,
      Q9.no_four_cycle_direct._native.native_decide.ax_1_1]
   ```

   There is no `sorry`, no `admit`, and no hand-written `axiom` declaration.  Full
   transcript: `lean/CHECK.log`; axiom output: `lean/AXIOMS.log`.

   **Negative control:** adding the single non-edge `(0,8)` (which closes 6 squares)
   makes Lean reject the file (`c4free = true` is evaluated to false, exit 1), so the
   check is not vacuous.

## Method

Public-source literature review (OEIS A245762, erdosproblems.com/86,
arXiv:2603.29127) → reformulate as a fully frustrated Ising / odd-square problem on Q₉ →
computational search over the 512-spin configurations (simulated annealing; 18 independent
runs reached 1526–1532 and found 1532 twice) → reconstruct the spin configuration from the
edge list → exhaustive verification (three Python checkers + Lean).  This odd-square
construction family goes back to Derrida–Pomeau–Toulouse–Vannimenus (1979) for n ≤ 7 and
Marinari–Parisi–Ritort (1995) for n = 8; the certificate here is an explicit n = 9 member.

## Scope and non-claims

* **Lower bound only**: f(9) ≥ 1532.  It does **not** determine f(9), does **not** prove
  optimality, and does **not** address the asymptotic conjecture of Erdős #86.
* **No priority claim.**  The comparison is against *public, indexed* sources as of
  **2026-10-18**; private or unindexed work (in particular old statistical-physics
  computations of ground states of the fully frustrated Ising model) may exist.
* The maximum of the odd-square family on Q₉ is **not** claimed to be 1532; eighteen
  seeded tabu searches found nothing above 1532 in this family, which is evidence, not proof.
* This work is **AI-assisted** — see below.

## Relation to prior public work (as of 2026-10-18)

| Source | public Q₉ lower bound | date | note |
|---|---|---|---|
| GitHub `rafalwronapl/erdos86-hypercube-c4` | 1505 | 2026-05 | explicit certificate |
| Erdős Problem a Day, Q9 write-up | 1531 | 2026-08-11 | AI-assisted, unreviewed; its text states attempts to reach 1532 failed |
| OEIS A245762 | no a(9) term | last edit 2026-09-02 | data only a(1..6); comments up to a(8) |
| **this repository** | **1532** | 2026-10-18 | **+1 over the best public claim we could find**; lower bound only |

We do not claim 1532 is the record, the first, or the best possible value.

## AI disclosure

This work was **AI-assisted**.  The computational search and the draft Python/Lean
scaffolding were produced by AI agents under human direction; the human author selected the
problem and the method (fully frustrated construction), directed the search, independently
re-verified the certificate (separate Python verifier and Lean run, see
`LEAD_VERIFICATION.md`), wrote the verification record, and is responsible for the claims.
Judgement of the certificate should rest on the explicit edge list and the standalone
verifiers, not on authorship.

## Authorship, date, repository

* Author: **Bil812** (GitHub)
* Date: **2026-10-18**
* Repository: <https://github.com/Bil812/erdos86-q9-c4> (tag **`v1.0`**)
* Declaration template and the three-tier wording guidance: `DECLARATION.md`
* Independent verification record: `LEAD_VERIFICATION.md`
* File hashes: `MANIFEST.sha256`

## Files

| path | content |
| --- | --- |
| `edges_q9_1532.txt` | the witness: 1532 Q9 edges, C₄-free |
| `q9b_spin_6.txt` | second, different 1532-edge solution |
| `spins_q9.txt` | 512-bit spin configuration generating the witness |
| `RESULTS.md` | detailed write-up: comparison, verification, structure |
| `verifiers/` | independent Python verifiers + self-tests (Q3 known-answer test) |
| `lean/Q9Witness.lean` | Lean 4 certificate (self-contained) |
| `lean/CHECK.log` | Lean run transcript + negative control |
| `lean/AXIOMS.log` | `#print axioms` output (`native_decide` axioms) |
| `DECLARATION.md` | declaration templates (standard / conservative / red lines) |
| `LEAD_VERIFICATION.md` | independent human-side verification record |
| `notes/REPORT_zh.md` | full session report (Chinese) |
| `notes/` | negative results from the same session (Q7/Q8, A276661) — clearly labelled |
| `submission/` | community-submission texts (Erdős Problem a Day, OEIS comment draft, email) |

## Citation

```bibtex
@misc{exq9c4_1532,
  title  = {An explicit 1532-edge C4-free subgraph of the 9-dimensional hypercube},
  author = {Bil812},
  year   = {2026},
  note   = {Lower bound f(9) >= 1532; Python verifiers and a Lean 4 certificate;
            AI-assisted, see README},
  url    = {https://github.com/Bil812/erdos86-q9-c4}
}
```

## License

MIT — see `LICENSE`.
