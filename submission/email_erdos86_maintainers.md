Subject: Erdős #86, Q9: explicit C4-free subgraph with 1532 edges (lower bound f(9) >= 1532)

Dear maintainers of Erdős Problems #86,

I would like to submit for verification an explicit finite certificate for the Q9 case of
Erdős problem #86 (C4-free subgraphs of the hypercube).

Claim (lower bound only): f(9) >= 1532, where f(n) = ex(Q_n, C4).

Certificate: an explicit edge list of 1532 edges on the 512 vertices of Q9 (each pair
differs in exactly one bit).  All C(9,2) * 2^7 = 4608 square faces of Q9 were enumerated and
none is complete.  A second, different 1532-edge solution is also included.

  file:     edges_q9_1532.txt
  SHA-256:  D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1
  repo:     https://github.com/Bil812/erdos86-q9-c4   (tag v1.0)

Verification is dependency-free Python:

  python verifiers/verify_c4_cycles.py edges_q9_1532.txt --n 9
  python verifiers/verify_c4_common_neighbours.py edges_q9_1532.txt --n 9
  python verifiers/redteam_audit_verify.py c4_9 edges_q9_1532.txt

There is also a self-contained Lean 4 certificate (lean/Q9Witness.lean, Lean 4.35.0) which
proves Q9.ex_Q9_C4_at_least_1532 with native_decide; the native evaluation axioms are
explicitly disclosed in lean/AXIOMS.log, and a negative control is rejected as expected.

Scope: this is a lower bound only.  It does not determine f(9), does not prove optimality,
and does not address the asymptotic question.  The construction is the odd-square / fully
frustrated Ising family (DPTV 1979 for D <= 7, MPR 1995 for D = 8 per arXiv:2603.29127 v5);
we make no priority claim and cannot exclude unindexed work.

Relation to public work we could find (as of 2026-10-18): 1505 (explicit GitHub certificate,
May 2026) and 1531 (Erdős Problem a Day, 2026-08-11, unreviewed).  OEIS A245762 has no a(9)
term.  This is +1 over the best public claim we could find.

Provenance / AI disclosure: this work was produced by AI agents (DeepSeek Harness,
deepseek-flash) operated from the account Bil812. The human account owner's role was
limited to initiating the task, approving the direction, and authorising publication; the
human did not do the mathematics and did not run or check the verifiers. AI errors are
possible and independent reproduction is welcome.

If useful, the account can provide any additional format (e.g., a CNF/DRAT-style certificate of
C4-freeness) or run further checks.

Best regards,
Bil812
https://github.com/Bil812/erdos86-q9-c4
