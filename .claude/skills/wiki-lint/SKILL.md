---
name: wiki-lint
description: |
  Run a health check on the wiki/ directory: find orphan pages, missing
  cross-links, contradictions, low-density nodes, god-nodes (high-inlink
  but thin pages), and inferred-link-heavy pages. Score 0-100 and report
  fixes — but do NOT auto-apply fixes. Use when the user says:
  「巡 wiki」「lint wiki」「健康度」「健康度檢查」「check wiki」
  「找孤兒」「檢查 wiki」「wiki 巡檢」.

  v1.3.2: 加入 cross-domain basename 衝突偵測（同 basename 在多個 domain → 歧義）
  v1.2: 加入 god-node 偵測（高 inlink 但內文薄弱的頁）+ 推斷連結密度檢查（[[X]] ?? 占比過高的頁）。

  Output is a markdown report with prioritized fix suggestions. The user
  reviews and approves fixes before any modification.
allowed-tools: [Read, Glob, Grep, Bash]
---

# wiki-lint

Run a health check on `wiki/`. Report problems with fix suggestions. **Do not auto-apply fixes** — wait for user approval.

## When this skill triggers

User says: 「巡 wiki」「lint wiki」「健康度」「健康度檢查」「check wiki」「找孤兒」「檢查 wiki」「wiki 巡檢」.

## Steps

### 1. Locate the wiki/ directory

`Glob wiki/entities/*.md` and `Glob wiki/maps/*.md`. If no entities found, report and exit.

### 2. Run the lint script

Execute `lint.py` (in same dir as this SKILL.md) via Bash. Use `${CLAUDE_PLUGIN_ROOT}` if available, otherwise the script will be at the same dir as this SKILL.md:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/wiki-lint/lint.py /path/to/vault/wiki
```

The script outputs JSON (v1.2):

```json
{
  "total_pages": 82,
  "orphans": ["..."],
  "missing_links": {"X": ["referrer1", "referrer2"]},
  "low_inlink_pages": [["年度結算流程", 1]],
  "hubs": [["Cowork", 29], ["Claude Code", 25]],
  "god_nodes": [
    {"name": "Cowork", "inlinks": 29, "words": 524, "ratio": 18.1, "severity": "warn"}
  ],
  "inferred_link_pages": [["X", 4, 7, 57.1]],
  "collisions": [{"basename": "X", "paths": ["orders/concept/X.md", "claude/concept/X.md"], "count": 2}],
  "score": 66,
  "score_breakdown": {
    "orphans": 16, "missing": 0, "density": 12,
    "hubs": 16, "godnodes": 12, "collisions": 20
  }
}
```

### 3. Filter false positives

The lint script may flag:
- Cross-folder references like `[[40-Resources/訂單系統/...]]` — these are LEGITIMATE, filter out
- Markdown table escape patterns like `[[X\|Y]]` — strip trailing `\` before checking
- Self-references — already filtered by script

See `references/HEALTH_RULES.md` for the full filter list.

### 4. Categorize issues (v1.2 加 god-node 與推斷連結)

Group into priority tiers:

**🔴 High priority** (multiple-page references, fix first):
- Missing concepts referenced ≥2 times
- True orphans
- **God nodes (critical)**：inlinks ≥ 8 且 words < 200 且 ratio < 25 — 樞紐概念但內文薄弱
- **Cross-domain basename collisions**（v1.3.2 新）：同 basename 出現在多個 domain/type 路徑下 → `[[X]]` 變歧義

**🟡 Medium priority** (single-reference issues):
- Missing concepts referenced once
- Pages with `inlinks=1` that could benefit from cross-references
- **God nodes (warn)**：inlinks ≥ 8 且只有 words 或 ratio 之一不及格
- **推斷連結比例偏高**（≥ 50% 的 outlinks 標 `??`）

**🔧 Writing-style errors** (not concepts, just markdown):
- `[[script.py]]` should be inline code
- `[[Migration_name]]` for non-concept names
- `[[X#anchor]]` opportunities (currently flat)
- `## 相關概念` 沒有分強/推/外部三組（v1.2 規範）

**ℹ️ Informational** (no action needed):
- Top hubs (just confirms structure is healthy)
- Type distribution
- Total stats

### 5. Generate fix suggestions (DO NOT APPLY)

For each issue, propose a specific fix. Examples:

> 🔴 [[公告系統]] missing — referenced by [[DiscountReviewService]], [[折扣審核流程]], [[通知系統]]
>   **Fix**: Create `wiki/entities/公告系統.md` describing the order system's announcement feature

> 🔴 [[Cowork]] is a god node — 29 inlinks but only 524 words (ratio 18.1)
>   **Fix**: 擴充 wiki/entities/Cowork.md，把它從「索引頁」升級為「概論頁」（建議 1500+ 字、加入分類示意圖、覆蓋 8 個主要主題）

> 🌫 Orphan: [[wiki/maps/Claude 學習地圖]]
>   **Fix**: Add `[[Claude 學習地圖]]` link in `wiki/entities/Cowork.md` "相關概念" section

> 🟡 [[X]] 推斷連結占 60%（4/7 條 ??）
>   **Fix**: Read X，逐條判斷 `??` 連結是否該升級為強連結（移除 `??`）或刪除

> 🔴 [[X]] collision — appears at `orders/concept/X.md` and `claude/concept/X.md`
>   **Fix**: 重命名其中一個（例：`orders/concept/X.md` → `orders/concept/X (訂單).md`）+ 改所有引用該歧義名的地方

> 🔧 `[[gen_import.py]]` — should be inline code
>   **Fix**: Replace with `` `gen_import.py` `` in 退款審核流程, OrderRepository

### 6. Report

Output a structured report:

```markdown
## 🏆 wiki/ Lint Report — Health: NN/100

### Summary

| Indicator | Value |
|-----------|-------|
| Total pages | 82 |
| Orphans | 0 |
| Missing concepts | 0 |
| Low-inlink pages | 7 |
| **God nodes** | **4 (warn)** |
| **Inferred-heavy pages** | **0** |
| Top hub | Cowork (29 inlinks) |

### 🔴 High Priority (N items)

[list with fix suggestions]

### 🏛 God Nodes — 樞紐概念待擴充

| Page | Inlinks | Words | Ratio | Severity | 建議 |
|------|---------|-------|-------|----------|------|
| Cowork | 29 | 524 | 18.1 | warn | 擴充至 ≥ 1500 字 |

### 🟡 Medium Priority (N items)

[list]

### 🔧 Writing Errors (N items)

[list]

### 🌫 Orphans (N items)

[list]

### ⭐ Healthy Signals

- Top 5 hubs all have ≥10 inlinks
- 96% of pages have inlinks
- Cross-topic density looks good
- 推斷連結比 < 30% — 連結品質高

### Recommended Action

Choose:
1. **Full repair** — apply all fixes
2. **High-priority only** (含 god node 擴充)
3. **God nodes only** — 集中擴充樞紐頁
4. **Writing errors only**
5. **No changes** (just keep report)
```

### 7. Append to wiki/log.md

```
| YYYY-MM-DD | Lint | - | - | Health NN/100. M orphans / N missing / G god nodes / I inferred-heavy. Awaiting user approval. |
```

## Rules (strict)

- **Never auto-apply fixes.** Always wait for user approval.
- **Always run the lint script** — don't manually count from Read calls (slow + error-prone).
- **Show category counts** — don't hide low-priority issues; let user see full picture.
- **Score is approximate** — don't promise specific numbers or trend over time without recomputing.
- **God nodes are recommendations, not bugs** — 一頁 inlinks 多但字少不一定是錯，可能只是索引頁。判斷時要看內容性質。

## See also

- `references/HEALTH_RULES.md` — what counts as orphan / missing / hub / god node, and false-positive filters
- `lint.py` — the Python lint script (run via bash)
