# f(9) ≥ 1532 — an explicit certificate at the 1994 Marinari–Parisi–Ritort value

> **Claim (lower bound only).** We exhibit an explicit C₄-free subgraph of the 9-dimensional
> hypercube Q₉ with **1532 edges**, so **f(9) ≥ 1532**, where f(n) = ex(Qₙ,C₄) is the maximum
> number of edges in a C₄-free subgraph of the n-cube.
>
> **The number is not new.**  A 1,532-edge C₄-free subgraph of Q₉ was *reported* by
> Marinari, Parisi and Ritort (cond-mat/9410089, 1994) as an annealing result
> (energy per spin −0.4947916…, i.e. 1,532 satisfied bonds of 2,304), **without publishing a
> configuration**.  What is new here, as far as public/indexed sources show, is an **explicit,
> reproducible certificate** at that value (and a Lean 4 check of it).  This is **not** a new
> lower bound for the literature, **not** a determination of f(9), and **not** a resolution of
> the asymptotic Erdős #86 question.  No priority over the 1994 value is claimed.
>
> **Provenance:** the entire research workflow was carried out by **AI agents**; the human
> account owner only initiated the task and authorised publication. See *Provenance* below.

## Independent verification (2026-10-24)

Erdős Problem a Day re-checked the certificate with **their own code** (none of this
repository's code was run) and replied **VERIFIED — as a certificate**:

* both graphs have 1,532 edges and no 4-cycle (two independent instruments: explicit
  four-cycle enumeration, and adjacency-matrix codegrees ≤ 1);
* every face carries one or three edges (784 and 3,824 faces) — the odd-square / fully
  frustrated signature; the two graphs share 1,024 edges;
* under the Marinari–Parisi–Ritort coupling J(x, x+e_ν) = (−1)^(Σ_{μ<ν} x_μ), the spin state
  in `spins_q9.txt` has exactly these 1,532 satisfied bonds, with energy per spin
  −95/192 = −0.4947916…, reproducing the 1994 printed value to every digit;
* **priority correction:** the number 1,532 was reported in 1994; this repository is (as far
  as they found) the first *public explicit certificate* at 1,532, not a new number.  Their
  earlier 1,531 page has been corrected accordingly.
* They did **not** check the Lean file.

Summary preserved as `REVIEW_2026-10-24.md`.

## Witness

* Edge list: **`edges_q9_1532.txt`** — 1532 lines `u v` with `0 ≤ u < v < 512` and Hamming
  distance exactly 1; 1532 distinct edges.
* **SHA-256**: `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`.
  The repository stores all files byte-for-byte (`.gitattributes` sets `* -text`), so this
  hash refers to the exact bytes you get from GitHub; `MANIFEST.sha256` lists every file.
* The graph is the set of satisfied ("positive") edges of a fully frustrated (odd-square)
  Ising configuration on Q₉: each of the 4,608 square faces carries exactly 1 or 3 edges.
  The 512-spin configuration is in `spins_q9.txt`.
* A **second, different** 1532-edge solution is included as `q9b_spin_6.txt`; it shares
  1,024 of its 1,532 edges with the first and passes the same checks.

## Verification

All commands are dependency-free Python 3 except the Lean check.

1. **Cycle enumeration** (all `C(9,2)·2⁷ = 4608` square faces):

   ```
   python verifiers/verify_c4_cycles.py edges_q9_1532.txt --n 9
   -> VERIFIED n=9 kept=1532 cycles=4608
   ```

2. **Common-neighbour criterion** (C₄-free ⟺ every vertex pair has ≤ 1 common neighbour):

   ```
   python verifiers/verify_c4_common_neighbours.py edges_q9_1532.txt --n 9
   -> VERIFIED (common-neighbour criterion)
   ```

3. **Red-team verifier** (different author, from the mathematical definition):

   ```
   python verifiers/redteam_audit_verify.py c4_9 edges_q9_1532.txt
   -> RESULT: PASS (C4-free)
   ```

4. **Lean 4** (Lean 4.35.0, x86_64-w64-windows-gnu, commit `eb6cafb7`), self-contained file
   `lean/Q9Witness.lean` (only `import Init`, no Mathlib):

   ```
   lean lean/Q9Witness.lean
   -> "Q9 witness checked: ex(Q9, C4) >= 1532"
      exit code 0
   ```

   The theorem is `Q9.ex_Q9_C4_at_least_1532 :
   edges.length = 1532 ∧ edges.all validEdge = true ∧ c4free = true`.

   **Trust caveat (disclosed on purpose):** the proof uses `native_decide` (trusted native
   evaluation, not a kernel reduction).  `#print axioms` shows the evaluation axioms, not only
   the three standard ones:

   ```
   'Q9.ex_Q9_C4_at_least_1532' depends on axioms:
     [Q9.edges_all_valid._native.native_decide.ax_1_1,
      Q9.edges_length._native.native_decide.ax_1_1,
      Q9.no_four_cycle_direct._native.native_decide.ax_1_1]
   ```

   No `sorry`, no `admit`, no hand-written `axiom`.  See `lean/CHECK.log` and
   `lean/AXIOMS.log`.  **Negative control:** adding the non-edge `(0,8)` (which closes six
   squares) makes Lean reject the file, so the check is not vacuous.

## Where it sits

* General lower/upper window for n = 9: **1532 ≤ f(9) ≤ 1584**.  The upper bound is the
  subcube-averaging inequality ex(Qₙ) ≤ 2n/(n−1)·ex(Qₙ₋₁) applied with the published
  ex(Q₇,C₄) ≤ 308: ex(Q₈) ≤ 704, ex(Q₉) ≤ ⌊18/8·704⌋ = 1584.
* **Odd-square family bound:** odd-square edge sets in Q₉ cannot exceed **1,536** (a field
  bound: every degree would have to be 6).  MPR (1994) did not reach it; whether 1,536 is
  attained is open (Minamoto, arXiv:2603.29127 v5, Open Problem 7).  Our own search — 18
  independent spin-annealing runs plus 18 seeded tabu searches — plateaued at 1,532, which is
  consistent with the 1994 annealing result.
* So the remaining finite question in this family is 1,533–1,536; we do not claim any of it.

## Relation to prior work

| Source | Q₉ lower bound | date | note |
|---|---|---|---|
| Marinari–Parisi–Ritort, cond-mat/9410089 | **1532** (reported) | 1994 | annealing value, energy per spin −0.4947916…; **no configuration published** |
| GitHub `rafalwronapl/erdos86-hypercube-c4` | 1505 | 2026-05 | explicit certificate |
| Erdős Problem a Day, Q9 write-up | 1531 | 2026-08-11 | explicit certificate; page since corrected (its 1,532 attempts had failed) |
| OEIS A245762 | no a(9) term | last edit 2026-09-02 | data only a(1..6); comments up to a(8) |
| **this repository** | **1532** (explicit) | 2026-10-18 | explicit certificate + Lean at the MPR-1994 value; verified 2026-10-24 |

## Method

Public-source literature review (OEIS A245762, erdosproblems.com/86,
arXiv:2603.29127) → reformulation as a fully frustrated Ising / odd-square problem on Q₉ →
simulated annealing over the 512-spin configurations (18 independent runs; best 1,532, found
twice) → reconstruction of the spin configuration from the edge list → exhaustive
verification (three Python checkers + Lean).  The construction family is due to
Derrida–Pomeau–Toulouse–Vannimenus (1979, D ≤ 7) and Marinari–Parisi–Ritort (1994/1995,
D = 8 and the D = 9 energy reported in 1994); Minamoto's v5 §6 transcribes the value.

## Scope and non-claims

* **Lower bound only**: f(9) ≥ 1532.  It does **not** determine f(9), does **not** prove
  optimality, and does **not** address the asymptotic Erdős #86 question.
* **No priority for the number**: 1,532 was reported in 1994.  The contribution is an explicit
  public certificate (and machine checks) at that value.
* The comparison to other public work is as of **2026-10-24** and covers public/indexed
  sources only.
* The maximum of the odd-square family on Q₉ is **not** claimed to be 1,532 (the field bound
  is 1,536 and attainment is open).
* This work is **AI-produced** — see below.

## Provenance (AI disclosure)

**This work was produced by AI agents; it is not human mathematical work.**  Problem
selection, literature audit, the fully frustrated construction, the spin search, the three
independent verifiers, the Lean formalisation (including obtaining the Lean toolchain), and
this write-up were all done by AI agents (DeepSeek Harness, model `deepseek-flash`) operated
from the account `Bil812`.  The human account owner's role was limited to initiating the
task, approving the general direction, and authorising publication; the human did **not** do
the mathematics, did **not** run or check the verifiers, and claims no authorship of the
result.  AI errors are possible, and independent reproduction is welcome.  The certificate
should be judged only on the explicit edge list and the standalone verifiers.

## Date, repository, versioning

* Produced by: **AI agents** (DeepSeek Harness, `deepseek-flash`), account **Bil812**
* Account owner / publisher: **Bil812** (initiated the task, authorised publication; no
  mathematical contribution)
* Date: **2026-10-18**; corrected **2026-10-24** after independent review
* Repository: <https://github.com/Bil812/erdos86-q9-c4> — tag **`v1.1`** (current);
  tag `v1.0` is the version submitted for review
* Re-verification record: `LEAD_VERIFICATION.md` (separate AI agent; not a human check)
* Independent community review: `REVIEW_2026-10-24.md`
* File hashes: `MANIFEST.sha256`

## Files

| path | content |
| --- | --- |
| `edges_q9_1532.txt` | the certificate: 1532 Q₉ edges, C₄-free |
| `q9b_spin_6.txt` | second, different 1532-edge solution (shares 1024 edges) |
| `spins_q9.txt` | 512-bit spin configuration generating the certificate |
| `RESULTS.md` | detailed write-up: verification, structure, position |
| `verifiers/` | independent Python verifiers + self-tests (Q3 known-answer test) |
| `lean/Q9Witness.lean` | Lean 4 certificate (self-contained) |
| `lean/CHECK.log` | Lean run transcript + negative control |
| `lean/AXIOMS.log` | `#print axioms` output (`native_decide` axioms) |
| `REVIEW_2026-10-24.md` | independent community verification verdict (2026-10-24) |
| `DECLARATION.md` | declaration templates (standard / conservative / red lines) |
| `LEAD_VERIFICATION.md` | re-verification record (separate AI agent; not human) |
| `notes/REPORT_zh.md` | full session report (Chinese) |
| `notes/` | negative results from the same session (Q7/Q8, A276661) |
| `submission/` | community-submission texts (kept for the record) |

## References

* M. Marinari, G. Parisi, F. Ritort, *The fully frustrated hypercubic model is glassy and aging
  at large D*, cond-mat/9410089 (1994), p. 4 (D = 9 energy per spin −0.494792…).
* M. Minamoto, *C₄-free subgraphs of the hypercubes Q₆, Q₇, Q₈: odd squares, fully frustrated
  models, and computational structure*, arXiv:2603.29127 v5 (2026), §6 and Open Problem 7.
* OEIS A245762 (maximum edges in a C₄-free subgraph of the n-cube).
* Erdős Problem a Day, #86 (2026), and the corrected 1,531 write-up.

## Citation

```bibtex
@misc{exq9c4_1532,
  title  = {An explicit 1532-edge C4-free subgraph of the 9-dimensional hypercube},
  author = {Bil812 (account holder) and DeepSeek Harness AI agents},
  year   = {2026},
  note   = {Explicit certificate for f(9) >= 1532, a value reported by
            Marinari-Parisi-Ritort (1994); Python verifiers and a Lean 4 certificate;
            AI-produced, see README},
  url    = {https://github.com/Bil812/erdos86-q9-c4}
}
```

## License

MIT — see `LICENSE`.
