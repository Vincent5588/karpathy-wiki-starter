# REPAIR_RULES.md

Detection logic, edge cases, and false-positive filters for each repair category.

## Auto-fixable categories

### 1. Broken `source:` paths

**What's broken:** frontmatter `source:` field references a path that doesn't exist on disk.

**Detection:**
1. Parse frontmatter, extract `source:` (or `sources:`) entries.
2. Strip `[[ ]]` wrappers and quotes.
3. Resolve path against vault root. If file doesn't exist, the path is broken.
4. URLs (`http://...`, `https://...`) are skipped — never broken in the filesystem sense.

**Auto-fix logic:**
1. Extract the basename (last path segment, strip `.md`).
2. `rglob("**/<basename>.md")` across the entire vault.
3. **Single match → auto-fix.** Rewrite frontmatter `source:` with new path.
4. **Multiple matches → review.** User picks.
5. **Zero matches → review.** User decides whether to remove or change to URL.

**False positives to avoid:**
- Don't flag URLs as broken.
- Don't flag paths that exist but use different case (Windows is case-insensitive).
- Don't flag paths missing `.md` extension if `<path>.md` exists.

**Idempotency:** Re-running on a fixed entity is a no-op (path exists → skip).

---

### 2. Missing frontmatter fields

**What's broken:** entity is missing one or more required v1.3 frontmatter fields:
`title`, `domain`, `type`, `status`, `created`, `updated`.

**Detection:**
- Parse frontmatter. Compute set difference vs. required fields.

**Auto-fix logic per field:**

| Field | Inference rule |
|-------|---------------|
| `domain` | Parent folder under `wiki/entities/` (e.g. `wiki/entities/orders/...` → `domain: orders`) |
| `type` | Grandparent folder (e.g. `wiki/entities/orders/system/...` → `type: system`) |
| `status` | Default `draft` |
| `aliases` | Default `[]` |

**Cannot auto-suggest** (review-only):
- `title` — content judgment
- `created` / `updated` — would need to fabricate dates
- `tags` — content judgment

**Edge cases:**
- Entity at `wiki/entities/<basename>.md` (flat root, no domain folder) → can't infer domain. Flag as `needs_review`.
- Entity has `domain: claude` but lives at `wiki/entities/orders/...` → don't auto-correct. Surface as `needs_review.frontmatter_mismatch`.
- Entire frontmatter block missing → all fields missing. `auto_fixable: false`.

**Idempotency:** Already-complete frontmatter → skip.

---

### 3. Dead links that already resolve (informational only)

**What's "broken":** wiki-lint reports `[[X]]` as a missing concept, but a file with basename `X` exists somewhere in the vault.

**Why this happens:** wiki-lint only scans `wiki/entities/` and `wiki/maps/` for available targets. If `X` exists at `40-Resources/X.md` or similar, lint won't see it as a target — but Obsidian does resolve the link by basename.

**Auto-fix logic:** **None.** This is purely informational. The link works as-is in Obsidian. The repair output just records that lint flagged it falsely.

**False positives:** None — this is itself a "false positive of lint" detection.

---

### 4. Orphan pages with backlink candidates

**What's broken:** entity has 0 inlinks (orphan), but other entities mention its basename in body text without using `[[ ]]` syntax.

**Detection:**
1. Take orphan list from lint output.
2. For each orphan name, scan all entity body texts (skip frontmatter and fenced code blocks).
3. Find mentions of the basename that are NOT inside `[[ ]]`.

**Auto-fix logic:**
- ≤2 candidates → auto-pick the one with most mentions, append `[[orphan]]` to its 「相關概念」 section.
- 3+ candidates → review (user picks).

**Where to insert the backlink:**
1. Look for `### 推斷連結（LLM 認為相關，待確認）` heading. If present, append `- [[orphan]] ?? — auto-added by wiki-repair`.
2. If only `### 強連結` exists, append there with a clear marker.
3. If no relations section exists at all, insert one before the closing `← 回到` line (or at end of body).

**False positives to avoid:**
- Don't flag mentions inside fenced code blocks.
- Don't flag mentions inside frontmatter (already stripped).
- Don't flag self-references.
- Don't double-count: if the entity already has a wiki-link to the orphan elsewhere, it's not a new mention.

**Idempotency:** After fix, the entity has a wiki-link → no longer counted as a "mention without link" → won't re-fire on next run.

---

## Needs-review categories

### 5. Contradictions (placeholder — not yet implemented)

**Future scope:** detect entities making conflicting claims about the same fact (e.g. `[[X]]` says "API at /v1/foo" but `[[Y]]` says "API at /v2/foo"). Requires NLP — out of scope for v1.3.1.

For now, repair.py returns an empty list. Use wiki-lint's manual review or wiki-query to surface contradictions.

---

### 6. God nodes — split suggestions

**What's broken:** entity has many inlinks (≥8) but thin body content (<200 words or words/inlinks ratio <25). Means the page is structurally important but informationally hollow.

**Detection:** Direct passthrough from lint output `god_nodes` array.

**Repair plan:**
- Per node, present current state (inlinks, words, ratio, severity).
- Suggest action:
  - `severity: warn` → expand body to ≥800 words
  - `severity: critical` → consider splitting into 2-3 atomic sub-pages

**Why review-only:** content design choice. Can't auto-split without understanding the topic structure.

---

### 7. Near-duplicate entities (placeholder — not yet implemented)

**Future scope:** detect entities with similar basenames or content (e.g. `年度結算流程` and `年度結算-流程`). Requires fuzzy matching — out of scope for v1.3.1.

For now, repair.py returns an empty list. Manually surface via lint reports.

---

## Cross-cutting rules

### Never rename basenames

Wiki-link resolution depends on basename stability. Repair never renames — only:
- Moves files (within same `<domain>/<type>/` only, and only if the user explicitly asks)
- Edits frontmatter
- Adds backlinks
- Edits body text where the basename is preserved

### Never auto-cross-domain

If a fix would involve moving an entity from `orders/` to `claude/` or similar, that's a content judgment. Always review.

### Atomicity

Apply fixes per category in order:
1. Frontmatter fixes (touches only frontmatter block — safe)
2. Source path fixes (touches frontmatter `source:` + body `§引用` references)
3. Backlink additions (touches body of *other* entities)

Within a category, process per-entity. If one edit fails, log and continue.

### Idempotency

Repair must be safely re-runnable. After a successful run, re-running detects no fixable issues (or strictly fewer than before). Use this as a smoke test.

---

## False-positive filters (cross-category)

Borrowed from wiki-lint's `HEALTH_RULES.md` and extended:

1. **Markdown table escapes**: `[[X\|Y]]` — strip trailing `\` before basename matching.
2. **Cross-folder paths**: `[[40-Resources/...]]`, `[[raw/...]]`, `[[wiki/...]]` — these are legitimate, not entity wiki-links. Don't suggest as "should be entity links".
3. **Standard files**: `[[README]]`, `[[index]]`, `[[Welcome]]`, `[[CLAUDE]]`, `[[Templates/...]]` — never count as entities.
4. **Self-references**: never count an entity's own basename mentioned in its own body as an "orphan candidate".
5. **Code blocks**: never count mentions inside `` ``` `` fenced blocks.
