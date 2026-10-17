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

- **Conservative (honest description):**
  > 我让 AI agent（DeepSeek Harness）对 Erdős #86 做了一次 Q₉ 有限下界计算：AI 构造出
  > 1532 条边的无 C₄ 子图，并经 Python 穷举与 Lean 4 验证，得 f(9) ≥ 1532（较公开可查
  > 最好 1531 +1，仅下界）。我的角色是提出任务并公开结果，数学与验证由 AI 完成。
- **Standard (README / submission):**
  > We exhibit an explicit C₄-free subgraph of Q₉ with 1532 edges, establishing the lower
  > bound f(9) ≥ 1532.  Certificate: `edges_q9_1532.txt` (SHA-256 `D701BD18…52A8B1`).
  > Verified by independent Python checkers (all 4608 four-cycles) and by Lean 4.35.0
  > (`native_decide`; evaluation axioms disclosed).  Lower bound only; no priority claim.
  > Produced by AI agents; the human account owner initiated the task and authorised
  > publication, and did no mathematical work.
