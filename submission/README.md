# Submission kit — Erdős #86, Q₉ lower bound f(9) ≥ 1532

Status: artifacts are public at <https://github.com/Bil812/erdos86-q9-c4> (tag `v1.0`).
This directory contains ready-to-paste texts for the community channels listed below.
Nothing here claims that the result has been reviewed or accepted anywhere.

## Order of operations (do not reorder)

1. **Timestamp first** — the public GitHub repository + tag is the timestamp. ✅ done.
2. **Then submit** to the channels below (one at a time, with the AI disclosure included).
3. **Wait for reproduction** before writing "submitted for community review" in a CV or
   interview; before that, write "constructed and self-verified".

## A. Erdős Problem a Day — submission form

<https://erdosproblemaday.com/submit>

Use the text in `erdosproblemaday_submission.md`.  This channel explicitly accepts
certificate-verification requests and is AI-disclosure friendly.  Attach / link:
`edges_q9_1532.txt`, SHA-256, and the one-command verifier.

## B. Erdős Problems #86 maintainers — email

Use `email_erdos86_maintainers.md`.  Keep it short: claim, one-line certificate,
verification command, link, scope, AI disclosure.  Do not attach large files; link them.

## C. OEIS A245762 — comment / edit proposal

Use `oeis_A245762_comment.txt`.  This is only a comment (`a(9) >= 1532`), it needs editor
review, and it must be phrased as a lower bound with the repository as the source.

## What NOT to write (red lines)

- ❌ "solved Erdős #86" / "resolved the hypercube Turán problem"
- ❌ "f(9) = 1532" / "ex(Q9,C4) = 1532"
- ❌ "first" / "world record" — only "+1 over the best public claim we could find as of
  2026-10-18", and the 1531 claim itself is unreviewed
- ❌ "pure kernel verification" / "only the three standard axioms" — the Lean proof uses
  `native_decide`; the evaluation axioms are listed in `lean/AXIOMS.log`
- ❌ "done independently" without mentioning AI assistance

## Safe one-liners

- **Conservative (CV / interview):**
  > 参与 Erdős #86（超立方体上的 C₄-free 子图问题）的 Q₉ 有限下界计算：在 AI agent
  > 辅助搜索下构造出 1532 条边的无 C₄ 子图，经 Python 穷举（4608 个 4-环）与 Lean 4
  > 双重验证，得到 f(9) ≥ 1532，较当时公开可查最好 1531 提高 1；只涉及有限情形，不涉及
  > 渐近猜想。证书与验证脚本已公开于 GitHub。
- **Standard (README / submission):**
  > We exhibit an explicit C₄-free subgraph of Q₉ with 1532 edges, establishing the lower
  > bound f(9) ≥ 1532.  Certificate: `edges_q9_1532.txt` (SHA-256 `D701BD18…52A8B1`).
  > Verified by independent Python checkers (all 4608 four-cycles) and by Lean 4.35.0
  > (`native_decide`; evaluation axioms disclosed).  Lower bound only; no priority claim.
  > AI-assisted; human author directed, verified and wrote up.
