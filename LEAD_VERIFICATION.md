# Independent re-verification — Q9, 1532-edge C4-free certificate

> **Provenance note.** "Lead" here is the AI orchestrator agent.  This re-check was run by a
> *different AI agent* than the one that found the witness (different verifier code, separate
> Lean run).  It is **not** a human verification: the human account owner did not run or
> check anything.  Judge the result from the reproduction commands below.

Date: 2026-10-18
Artifact under test:
- `research/c4-hypercube/edges_q9_1532.txt` (1532 lines, `u v`)
- `research/lean/Q9Witness.lean`

## 1. Certificate identity

- Edges: 1532 lines, 1532 distinct pairs, all `0 <= u < v < 512`, all `popcount(u^v) == 1`.
- SHA-256 of `edges_q9_1532.txt`:
  `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`

## 2. Independent Python verification (Lead's own verifier, not the team's)

Command:

    python verifiers/lead_verify_q9.py edges_q9_1532.txt 9

Output:

    n=9 vertices=512
    edges=1532  distinct=1532
    4-cycles enumerated=4608 (expected C(9,2)*2^7=4608)
    4-cycles with all 4 edges present=0
    pairs with >=2 common neighbours=0
    degree distribution={5:14, 6:494, 7:2, 8:2}
    per-direction edge counts=[168,170,170,170,174,170,170,170,170]
    RESULT: VALID C4-FREE

## 3. Lean check (independent run by Lead)

Toolchain: Lean 4.35.0 (x86_64-w64-windows-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc).
Command:

    lean lean/Q9Witness.lean

Result: exit code 0, prints `"Q9 witness checked: ex(Q9, C4) >= 1532"`.

Consistency:

- Lean `edges` list parsed and compared with the `.txt`: **identical sets**, 1532 = 1532, 0 differences.
- Source contains **no `sorry`**, **no `axiom` declaration**, **no `admit`**.
- Negative control `lean/CHECK.log (negative control)` (adds edge `(0,8)`, closing 6 squares): **fails**, exit code 1, with errors at `edges.length`, `c4free`, `edges_positive`, `certificate`. The check is non-vacuous.

`#print axioms` (Lead-appended copy `lean/AXIOMS.log`):

    'Q9.ex_Q9_C4_at_least_1532' depends on axioms:
      [Q9.edges_all_valid._native.native_decide.ax_1_1,
       Q9.edges_length._native.native_decide.ax_1_1,
       Q9.no_four_cycle_direct._native.native_decide.ax_1_1]
    'Q9.certificate_ok' depends on axioms: [Q9.certificate_ok._native.native_decide.ax_1_1]

## 4. Interpretation / caveats

1. **The theorem is real**: `ex_Q9_C4_at_least_1532 : edges.length = 1532 ∧ edges.all validEdge = true ∧ c4free = true`, checked by Lean 4.35.0, with a failing negative control.
2. **`native_decide` caveat**: the proof uses `native_decide`, so it trusts Lean's native evaluator (`Lean.ofReduceBool`-style axioms), **not** a pure kernel reduction. For finite certificates this is a common and defensible choice, but it is not the stricter "only `propext`, `Classical.choice`, `Quot.sound`" standard used in some community replays. Must be disclosed. To reach kernel-only, one would need a `decide`-based (kernel-evaluated) proof or a different certificate format — likely slow at this certificate size.
3. **Scope**: this is a **lower bound only**: `f(9) >= 1532`. It does not determine `f(9)`, does not prove optimality, and does **not** address the asymptotic Erdős #86 conjecture.
4. **Novelty (public-source check, 2026-10-17/18)**: best public Q9 lower bound found was **1531** (erdosproblemaday.com, 2026-08-11, AI-assisted, unreviewed, with public reproducer); earlier public certificate 1505 (rafalwrona GitHub); OEIS A245762 has no `a(9)`; erdosproblems.com #86 lists only Q7/Q8. So 1532 is **+1 over the best public claim**, subject to unindexed statistical-physics literature (odd-square / fully frustrated Ising) possibly containing `g(9)`.
5. **AI disclosure required**: the search was AI-agent driven; the write-up must say so.

## 5. Reproduce

    python verifiers/lead_verify_q9.py edges_q9_1532.txt 9
    lean lean/Q9Witness.lean
