# 成果声明模板（Q9, f(9) ≥ 1532）

> 用法：把 `【】` 换成你的信息。对外提交/README 用“标准档”，综评/面试用“保守档”，不要用“强档”。

---

## A. 一句话主张（最常用）

> 我构造了 9 维超立方体 Q₉ 上一个含 **1532 条边**、不含 4-环（C₄）的子图，并给出可复现的机器验证，因此 **f(9) ≥ 1532**（f(n) 为 Erdős #86 中的 C₄-free 最大边数）。

---

## B. 标准档：提交/README 完整声明

### Claim

We exhibit an explicit C₄-free subgraph of the 9-dimensional hypercube Q₉ with **1532 edges**, establishing the lower bound **f(9) ≥ 1532**, where f(n) = ex(Qₙ, C₄) is the maximum number of edges in a C₄-free subgraph of Qₙ.

### Witness

- Edge list: `edges_q9_1532.txt` — 1532 lines `u v` (0 ≤ u < v < 512, Hamming distance 1), 1532 distinct edges.
- SHA-256: `D701BD189B9C79466089A2A1F8601C2FCBF82833F0A7C717938C35DA1F52A8B1`.
- The graph is the set of positive edges of a fully frustrated (odd-square) Ising configuration on Q₉; every one of the 4608 square faces has exactly 1 or 3 selected edges.

### Verification

1. Python (independent verifier, `verify_q9.py`):
   - all 1532 lines are genuine Q₉ edges, no duplicates;
   - all C(9,2)·2⁷ = **4608** four-cycles enumerated, **0** fully present;
   - common-neighbour criterion: **0** vertex pairs at Hamming distance 2 with ≥ 2 common neighbours.
2. Lean 4 (Lean 4.35.0): `Q9Witness.lean` compiles with exit code 0; theorem
   `ex_Q9_C4_at_least_1532 : edges.length = 1532 ∧ edges.all validEdge = true ∧ c4free = true`;
   no `sorry`, no hand-written `axiom` (the `native_decide` evaluation axioms are disclosed in `lean/AXIOMS.log`); negative control (adding edge `(0,8)`) fails as expected.
   - Caveat: the Lean proof uses `native_decide` (trusted native evaluation), not a pure kernel reduction; `#print axioms` reports the three `native_decide` axioms, not the standard three only. This is disclosed.

Reproduce:

```
python verify_q9.py edges_q9_1532.txt 9
lean Q9Witness.lean
```

### Method

Literature review (OEIS A245762, erdősproblems.com/86, Minamoto arXiv:2603.29127) → restate as a hitting-set / frustrated-Ising problem on Q₉ → computational search over spin configurations (simulated annealing / local search) → extract positive-edge set → exhaustive verification (Python + Lean). The 1532-edge witness is one output of this pipeline; a second 1532-edge witness was also found.

### Scope and non-claims

- This is a **lower bound only**: f(9) ≥ 1532. It does **not** determine f(9), does **not** prove optimality, and does **not** address the asymptotic conjecture of Erdős #86.
- We make **no priority claim**: the comparison below is against public, indexed sources as of the stated date, and unindexed or private work may exist.
- The construction lies in the odd-square (fully frustrated) family; the maximum of that family on Q₉ is not claimed to be 1532.

### Relation to prior public work (as of 2026-10-18)

| Source | Q₉ lower bound | Date | Note |
|---|---|---|---|
| GitHub `rafalwronapl/erdos86-hypercube-c4` | 1505 | 2026-05 | explicit certificate |
| erdosproblemaday.com, Q9 | 1531 | 2026-08-11 | AI-assisted, unreviewed; text says attempts to reach 1532 failed |
| OEIS A245762 | no a(9) | — | a(1..6) only; comments to a(8) |
| This work | **1532** | 2026-10-17 | +1 over the best public claim found |

### AI disclosure

This work was **AI-assisted**. The computational search and the draft Lean/Python scaffolding were produced by an AI agent (AI agents (DeepSeek Harness, deepseek-flash)) under human direction; the human author (Bil812) selected the problem and method, directed the search, independently re-verified the certificate (Python and Lean on a separate machine/run), wrote the verification record, and is responsible for the claims. The certificate itself should be judged by the explicit edge list and the standalone verifiers, not by authorship.

### Authorship / date / priority

- Author: Bil812 (GitHub)
- Date: 2026-10-18
- Repository: https://github.com/Bil812/erdos86-q9-c4, commit tag v1.0 (commit hash: see git log / tag)
- This declaration is made public on 2026-10-18 to establish a timestamp for the certificate.

---

## C. 保守档：综评“其他研究经历”/面试用（2—3 句）

> 我参与了 Erdős #86（超立方体上的 C₄-free 子图问题）的 Q₉ 有限下界计算：在 AI agent 辅助搜索下，构造出一个 1532 条边的无 C₄ 子图，并用 Python 穷举（4608 个 4-环）和 Lean 4 形式化双重验证，得到 f(9) ≥ 1532，较当时公开最好结果 1531 提高 1。该工作只给出下界，不涉及渐近猜想；证书与验证脚本已已公开于 GitHub。

面试一句话：

> 我用 AI 做计算搜索、用 Lean 做机器验证，找到了一个问题的一个 +1 下界——重点不是那 1 条边，而是“AI 产出 + 可独立复核”的流程。

---

## D. 红线：这些话不能说

- ❌ “我解决了 Erdős #86 / 超立方体 Turán 问题” → 只解决了 n=9 的一个下界。
- ❌ “ex(Q₉, C₄) = 1532 / 精确值” → 只是下界。
- ❌ “首次 / 世界纪录” → 只能说“截至2026-10-18可查公开来源中最好”，且 1531 本身未评审。
- ❌ “纯 kernel 验证 / 只依赖三条标准公理” → 用了 `native_decide`，要说明。
- ❌ “独立完成 / 没有用 AI” → 必须披露 AI 辅助。
- ❌ “这是奥赛/科研水平的突破” → +1 的有限下界，别拔高。

---

## E. 发布步骤（按顺序）

1. **先固定工件**：每个文件算 SHA-256（见 MANIFEST.sha256）；写 README（含上文的 Claim/Witness/Verification/Scope/AI disclosure）；`git init` + commit + tag，记录 commit hash 和日期。
2. **先公开时间戳**：推到 GitHub（public）或先发一个公开 gist；不要先发社媒长文。
3. **再提交社区**：
   - `erdosproblemaday.com/submit`（他们收“证书验证请求”，对 AI 披露友好）；
   - 邮件给 Erdős Problems #86 维护者（论坛评论目前暂停）；
   - 可选：OEIS A245762 加评论 `a(9) >= 1532`（需编辑审核，且只是下界）。
4. **等待复核**：如果他们复现通过，再在综评/面试里写“已提交社区复核”；在此之前写“已构造并自验”。
5. **不要**在提交前声称“已被验证/已被接受”。

---

## F. 文件清单（提交时一并附上）

- `edges_q9_1532.txt`（证书，含 SHA-256）
- `verify_q9.py`（独立 Python 验证器）
- `Q9Witness.lean`（Lean 4 证书）
- `lean/CHECK.log` / `lean/AXIOMS.log`（`#print axioms`）/ 负控制失败输出
- `LEAD_VERIFICATION.md`（本次独立复核记录）
- `README.md`（本文 B 档）
- `LICENSE`（建议 MIT/CC0，便于复核）
