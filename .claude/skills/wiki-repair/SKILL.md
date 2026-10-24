---
name: wiki-repair
description: |
  Apply safe, structural fixes to a karpathy-wiki-pattern wiki — repair broken
  `source:` paths, fill missing v1.3 frontmatter (domain/status), redirect dead
  `[[wiki-links]]` that resolve by basename elsewhere, and add backlinks for
  orphans with obvious candidates. Bigger judgment calls (contradictions, god-node
  splits, duplicate merges) are surfaced as a plan for user approval — never
  auto-applied. Use when the user says: 「修 wiki」「修補 wiki」「wiki 修復」
  「fix wiki」「批量修 wiki」「wiki repair」「批准 lint 的修補」「跑 repair」.

  Pairs with wiki-lint: lint detects + reports, repair categorizes into
  auto-fixable vs needs-review and applies after dry-run approval.

  Output: an audit report at wiki/reports/REPAIR_YYYYMMDD_HHmm.md plus a
  wiki/log.md entry summarizing what changed.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# wiki-repair (v1.3.1)

Apply structural fixes to the wiki. Always dry-run first, always wait for user approval, always log.

## When this skill triggers

User says: 「修 wiki」「修補 wiki」「wiki 修復」「fix wiki」「批量修 wiki」「wiki repair」「批准 lint 的修補」「跑 repair」.

## What this skill fixes

### Auto-fixable (executed in one batch after approval)

| # | Issue | Detection | Fix |
|---|------|----------|-----|
| 1 | `source:` path 壞掉 | frontmatter `source:` 指到不存在的檔案 | grep vault 找同 basename 的實際位置，改寫 source |
| 2 | frontmatter 缺 v1.3 必填欄位 | 缺 `domain` / `type` / `status` 之一 | 推論補上（domain 從父資料夾、type 從父資料夾、status 預設 `draft`） |
| 3 | 死 `[[link]]` 但 basename 在 vault 找得到 | lint 報 missing，但 grep 找到同 basename 的實際 entity | 不改原連結（因為 Obsidian 解析還是會通），但記錄供使用者確認 |
| 4 | 孤兒頁有合理 backlink 候選 | lint 報 orphan，但有 entity 內文提到這個 basename（沒包 `[[]]`） | 在候選頁加 `[[orphan]]` 連結 |

### Needs human review (plan-only, no auto-apply)

| # | Issue | Plan content |
|---|------|--------------|
| 5 | 同基底矛盾聲明 | 列衝突點 + 兩種版本，問使用者選哪個 |
| 6 | god node | 列拆分建議（建議切成幾個 atomic + 主題分配） |
| 7 | 重複 entity（近似 basename） | 列合併 / 改名候選 |

### Out of scope (不修)

- 內容語意問題（這是 ingest 的事）
- type 詞彙不是 v1.3 標準（這是 backfill 的事 — 用 wiki-ingest Mode B）
- index.md 結構整理（這是 wiki-compile 或手工的事）

## Pipeline

### 1. Locate vault and lint output

```bash
# Find vault root (look for wiki/entities/)
# Try recent lint output first:
LATEST_LINT=$(ls -t wiki/reports/LINT_*.json 2>/dev/null | head -1)
```

If no recent lint JSON exists, **run wiki-lint first** to generate fresh data. Repair operates on lint's output — it doesn't re-implement detection.

### 2. Run the repair script

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/wiki-repair/repair.py \
  --vault /path/to/vault \
  --lint /path/to/lint.json \
  --plan-only > /tmp/repair-plan.json
```

`repair.py` outputs JSON with categorized issues:

```json
{
  "auto_fixable": {
    "broken_sources": [
      {"entity": "wiki/entities/orders/process/年度結算流程.md",
       "frontmatter_field": "source",
       "broken_path": "raw/01-articles/old-spec.md",
       "suggested_path": "20-Projects/X/sources/old-spec.md",
       "match_basis": "basename grep, 1 match"}
    ],
    "missing_frontmatter": [
      {"entity": "wiki/entities/claude/concept/X.md",
       "missing_fields": ["status"],
       "suggested_values": {"status": "draft"}}
    ],
    "dead_links_resolvable": [
      {"entity": "wiki/entities/A.md",
       "dead_link": "[[公告系統]]",
       "found_at": "wiki/entities/orders/system/公告系統.md",
       "note": "Obsidian resolves by basename — link works, no edit needed, just confirming"}
    ],
    "orphan_backlinks": [
      {"orphan": "wiki/maps/Claude 學習地圖.md",
       "candidates": ["wiki/entities/claude/system/Cowork.md",
                      "wiki/entities/claude/system/Claude Code.md"],
       "rationale": "Both reference 'Claude 學習地圖' in body text"}
    ]
  },
  "needs_review": {
    "contradictions": [],
    "god_nodes": [
      {"page": "wiki/entities/claude/system/Cowork.md",
       "inlinks": 29, "words": 524,
       "split_suggestion": "考慮拆成 Cowork 概論 + Cowork 工作流模式 + Cowork UI"}
    ],
    "near_duplicates": []
  },
  "stats": {"auto_count": 7, "review_count": 1}
}
```

### 3. Present plan to user

Show a markdown summary, grouped by fix category. Each row: what + why + after-state. Use this template:

```markdown
## 🔧 wiki-repair plan (dry-run)

### Auto-fixable (N items)

#### 1. Broken `source:` paths (N)
| # | Entity | Broken | → Suggested |
|---|--------|--------|-------------|
| 1 | orders/process/年度結算流程 | raw/01-articles/old-spec.md | 20-Projects/X/sources/old-spec.md |

#### 2. Missing frontmatter (N)
| # | Entity | Missing | Will fill |
|---|--------|---------|-----------|
| 1 | claude/concept/X | status | status: draft |

#### 3. Dead links that already resolve (N — informational)
[list — no edit needed]

#### 4. Orphan backlinks (N)
| # | Orphan | Will add link to |
|---|--------|-----------------|
| 1 | wiki/maps/Claude 學習地圖 | claude/system/Cowork (1 of 2 candidates) |

### Needs human review (N items)

[list with descriptions, no auto-apply]

---

**Reply:**
- `go` / `apply auto` → execute all auto-fixable in one batch
- `apply 1,4` → only fix categories 1 and 4
- `apply auto + review N` → auto + take action on review item N
- `cancel` → abort
```

### 4. Apply (only after explicit approval)

For each auto-fixable issue:

- **Broken sources**: read entity, replace_all the broken path with suggested path (frontmatter `source:` field + body `§引用`)
- **Missing frontmatter**: insert missing fields after `updated:` line (or at end of frontmatter block)
- **Orphan backlinks**: append `- [[orphan]] — auto-added by wiki-repair` under candidate entity's `### 強連結` or `### 推斷連結 ??` section
- **Dead links resolvable**: no file edit; just note in audit report

For needs-review items: only apply ones the user explicitly approved (`apply review N`).

### 5. Atomicity

- Process auto-fixes per category (sources first, then frontmatter, then backlinks). If any single edit fails, log the error and continue with the rest.
- Never write partial frontmatter (must produce valid YAML).
- Never rename a basename (would break wiki-links).

### 6. Write audit report

Save to `wiki/reports/REPAIR_YYYYMMDD_HHmm.md` using template at `references/REPORT_TEMPLATE.md`:

```markdown
# Repair Report — YYYY-MM-DD HH:MM

## Summary
| Category | Detected | Applied | Skipped |
|----------|----------|---------|---------|
| Broken sources | 3 | 3 | 0 |
| Missing frontmatter | 5 | 5 | 0 |
| Orphan backlinks | 2 | 1 | 1 |
| God nodes | 4 | 0 (review only) | 4 |

## Detail
[per-item changes with before/after]

## Files modified
- wiki/entities/orders/process/年度結算流程.md (source: rewritten)
- wiki/entities/claude/concept/X.md (frontmatter: +status)
- ...
```

### 7. Append to wiki/log.md

```
| YYYY-MM-DD | Repair | - | N entities modified | Auto: M sources / X frontmatter / Y backlinks. Review: K god nodes flagged. Report: [[wiki/reports/REPAIR_YYYYMMDD_HHmm]] |
```

## Rules (strict)

- **Never apply without explicit user approval.** Always dry-run + plan first.
- **Never rename a basename.** Wiki-link safety depends on this.
- **Never auto-merge entities across `<domain>/<type>` boundaries.** Cross-domain duplicates are review-only.
- **Always run wiki-lint first** (or accept fresh lint.json) — repair doesn't re-implement detection.
- **Idempotent.** Re-running on already-fixed issues should be a no-op (frontmatter already complete, sources already valid, etc.).
- **Single source of truth.** repair.py categorizes; the LLM applies. Don't duplicate detection logic in skill instructions.

## Edge cases

### Multi-match basename for source repair
Two `[[A]]` files exist (in different `<domain>/<type>`). Don't auto-pick — flag as `needs_review.cross_domain_basename`, list both, ask user.

### Frontmatter already has `domain` but it's wrong (e.g. file at `orders/system/X.md` but `domain: claude`)
**Don't auto-fix** — surface as `needs_review.frontmatter_mismatch`. Repair the frontmatter only when it's *missing*, not when it's *wrong* (which is a content judgment).

### Orphan has 5+ backlink candidates
Don't fan out. Flag as `needs_review` and let user pick the best 1-2.

### Lint hasn't been run for a while
If lint output is older than `--lint-stale-days` (default 7), warn and offer to re-run lint first.

## See also

- `references/REPAIR_RULES.md` — detailed detection logic for each fix category, edge cases, and false-positive filters
- `references/REPORT_TEMPLATE.md` — audit report layout
- `repair.py` — the detection / categorization script (run via bash)
