# REPORT_TEMPLATE.md

Audit report layout for wiki-repair runs. Save to `wiki/reports/REPAIR_YYYYMMDD_HHmm.md`.

## Template

```markdown
---
title: "Repair Report — YYYY-MM-DD HH:MM"
type: artifact
domain: wiki
status: stable
tags: [wiki, repair, audit]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 🔧 Repair Report — YYYY-MM-DD HH:MM

> wiki-repair v1.3.1 run audit. Lint baseline: `wiki/reports/LINT_<timestamp>.json`.

## Summary

| Category | Detected | Applied | Skipped (Review) | Failed |
|----------|----------|---------|------------------|--------|
| Broken sources | 5 | 5 | 0 | 0 |
| Missing frontmatter | 8 | 8 | 0 | 0 |
| Orphan backlinks | 3 | 2 | 1 | 0 |
| God nodes | 4 | 0 | 4 | 0 |
| Contradictions | 0 | 0 | 0 | 0 |
| **Total** | **20** | **15** | **5** | **0** |

## Files modified (N)

- `wiki/entities/orders/process/年度結算流程.md`
  - frontmatter `source:` rewritten: `raw/old.md` → `20-Projects/X/sources/old.md`
- `wiki/entities/claude/concept/X.md`
  - frontmatter: added `status: draft`
- ...

## Detail by category

### 1. Broken sources (5 applied)

| # | Entity | Before | After |
|---|--------|--------|-------|
| 1 | orders/process/年度結算流程 | raw/old.md | 20-Projects/X/sources/old.md |
| ... |

### 2. Missing frontmatter (8 applied)

| # | Entity | Field | Value |
|---|--------|-------|-------|
| 1 | claude/concept/X | status | draft |
| 2 | claude/concept/X | aliases | [] |
| ... |

### 3. Orphan backlinks (2 applied, 1 skipped)

#### Applied
| # | Orphan | Candidate that received backlink |
|---|--------|-----------------------------------|
| 1 | wiki/maps/Claude 學習地圖 | claude/system/Cowork.md |

#### Skipped (multiple candidates — needs user pick)
| # | Orphan | Candidates |
|---|--------|-----------|
| 1 | X | A, B, C |

### 4. God nodes (4 flagged, 0 applied — review-only)

| # | Page | Inlinks | Words | Ratio | Severity | Action suggested |
|---|------|---------|-------|-------|----------|-----------------|
| 1 | claude/system/Cowork | 29 | 524 | 18.1 | warn | Expand to ≥1500 words |

### 5. Informational (dead links that already resolve — N items)

These were flagged by lint as `missing_links` but Obsidian resolves them by basename. No edit needed.

| # | Link | Found at |
|---|------|---------|
| 1 | [[公告系統]] | wiki/entities/orders/system/公告系統.md |

## Re-lint recommended

After applying these fixes, run wiki-lint again to verify health score improved. Expected delta:
- orphans: -2 (backlink-fixed orphans no longer orphan)
- missing: 0 change (nothing structural changed for missing concepts)
- score: +N

## Notes

- All edits use UTF-8 (no BOM)
- Frontmatter writes preserve existing key order
- No basenames were renamed
- Backlink insertions used the entity's existing 「相關概念」 section style

← back to [[wiki/log|log.md]]
```

## Style notes

- Use clean prose, not log-noise. The report should be readable a year from now.
- Include before/after diffs only when the change is non-obvious.
- If 0 changes were applied (everything was review-only), the report can be very short — just summary table + "Nothing applied — see review items".
- Always link back to `wiki/log.md` and the source `LINT_*.json` for traceability.
