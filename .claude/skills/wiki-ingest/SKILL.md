---
name: wiki-ingest
description: |
  Extract atomic entities from raw notes and write them into a hierarchical
  wiki/entities/[domain]/[type]/ structure. Use when the user says
  「ingest」「process raw」「extract entities」, or drops new content into raw/.
  Also handles backfill of existing flat entities.

  v1.3: entity 自動推論 domain/type 落到資料夾；raw 檔 ingest 完搬去
  PARA 子路徑或 raw/09-ARCHIVE/YYYY-MM/，並改寫所有 entity 的 sources:。
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# wiki-ingest (v1.3.3 — staging)

Extract atomic concepts from raw, messy input and write them as well-formed wiki entities — **automatically classified into a domain/type folder hierarchy** so `entities/` never becomes a flat dumping ground.

## What changed in v1.3.3 (staging — pending plugin v1.4.5 release)

**Step 0 prerequisite added** for vault Rule P (Cite-or-Die Cascade Citation).

Before any vault write, LLM must explicitly cite the cascade plan from `[[Wiki_維護觸發規則]]` §1 in chat. This prevents the LLM-skips-cascade-and-nobody-notices failure mode that triggered Rule P codification (2026-05-12 same-day double miss: Hooks ingest skipped 4 cascade points; Scheduled Tasks augmentation skipped Wiki_主目錄).

→ See "Step 0: Rule P cite-or-die" added at the top of the Pipeline section below.

## What changed in v1.3.2

Two patches on top of v1.3.0:

1. **`wiki/index.md` is updated as part of every ingest** (was unwritten before — see step 7 below). Header counters (entity count, domain list, last-updated) and category lists both get bumped.

2. **`wiki-lint` (the sister skill) now detects cross-domain basename collisions.** If two entities under different `<domain>/<type>/` end up with the same basename, `[[X]]` becomes ambiguous. Lint surfaces these — `wiki-ingest` step 4 (collision check) was already supposed to prevent this, but lint is a backstop.

## What changed in v1.3.0

Three things:

1. **Entities are no longer flat.** Every entity is routed to `wiki/entities/<domain>/<type>/<entity-name>.md`, where `<domain>` and `<type>` are inferred from content — open vocabulary, not a fixed enum.

2. **Raw files are routed too.** After ingest, the original raw file is moved out of `raw/` into either a specific PARA folder (`20-Projects/<project>/sources/`, `30-Areas/<area>/sources/`, etc.) or the archive fallback `raw/09-ARCHIVE/YYYY-MM/`. The `sources:` frontmatter in every affected entity is updated to point to the new path.

3. **Backfill of existing flat entities** is supported as Mode B (one-time migration; see below).

## Inputs

- One or more files in `raw/` (or content the user pastes into the chat)
- Existing `wiki/entities/` tree (used to keep taxonomy consistent — reuse existing domain/type folder names whenever they fit)

## Outputs

- One `.md` file per atomic entity at `wiki/entities/<domain>/<type>/<slug>.md`
- Each file follows `references/ENTITY_TEMPLATE.md`
- Optional ingest log appended to `wiki/log.md`

## Pipeline

### Step 0: Rule P Cite-or-Die (v1.3.3 — MUST DO FIRST)

**Before reading any raw or writing any file**, LLM must output the following in chat:

```
依 [[Wiki_維護觸發規則]] §1，本次「ingest <raw 名稱>」將 cascade：
 ① wiki/entities/<domain>/<type>/<X>.md（強制 — 新建本體或 heuristic 2 補既有）
 ② wiki/daily/YYYY/MM/YYYY-MM-DD.md（強制 — daily log）
 ③ Wiki_主目錄「📥 最近 ingest 紀錄」+「📅 最後更新」+ domain 計數 +
    entity 總數（強制 × 4，補既有時計數不變只更前 2）
 ④ wiki/最新資料歷史/YYYY/YYYY-MM.md（強制 — ingest history hub；跨月時 LLM 自動建新月檔）
 ⑤ Wiki_儀表板 frontmatter `updated:` + 今日 H3（強制）
 ⑥ Wiki_健康度監控 frontmatter `updated:`（強制）
 ⑦ Wiki_專有名詞對照表（建議 — 若 entity 含未收錄的英文專有名詞）
 ⑧ WIKI_TODO（建議 — 衍生待辦）
 ⑨ PARA routing raw（強制 — 提案目的地 + 等批准 + 搬檔）

 自我檢查（ingest 完跑）：
   find wiki/entities -name '*.md' | wc -l           # entity 總數
   grep -c "$(date +%F)" Wiki_主目錄.md                # 主目錄今日提及
   grep -l "updated: $(date +%F)" Wiki操作文件/Wiki_*.md  # 監控檔 frontmatter bump
```

**為什麼**：vault [[CLAUDE]] §⚡ + 規則 P 規定。LLM 跳過 Step 0 → 違反 [[rule-P-cascade-citation|規則 P]] → 違反 [[Wiki_維護觸發規則]] §10「執行動作前 chat 自述要 cascade 哪些檔」。

**例外**：若使用者在同 session 明確說「直接做不必 cite」/「直接改」，可 skip Step 0。否則一律 cite。

**heuristic 2 變體**：若 Discovery 發現要 ingest 的主題有既有 stable entity 重疊 ≥ 70% → 改成「補既有」cite 格式（cascade 項目相同，只是 ① row 寫「補既有 [[X]]，補 source + 內容 + 規則 H 版本歷程」，計數不變）。

---

### Mode A — Standard ingest (default)

For each chunk of raw input:

1. **Identify atomic entities.** One concept = one entity. Split aggressively. If a heading has 3 sub-concepts that could each stand alone, that's 3 entities, not 1.

2. **For each entity, decide `domain` and `type` BEFORE writing:**

   a. **Read `references/ORGANIZATION.md`** for the inference rules (open vocabulary, kebab-case, reuse-first).

   b. **List existing folders** under `wiki/entities/` to see the current taxonomy. Example:
      ```
      wiki/entities/finance/process/
      wiki/entities/finance/artifact/
      wiki/entities/claude/concept/
      ```

   c. **Reuse-first rule:** if the new entity fits cleanly into an existing `<domain>/<type>` pair, use that exact pair. Do NOT invent a synonym (`finance-process`, `human-resources`, `procedure`) when an existing folder already covers it.

   d. **Coin a new value only when no existing folder fits.** Pick the most general name that's still meaningful — `concept` over `concept-explanation`, `claude` over `claude-code-workflow`.

   e. **Both values are kebab-case ASCII.** Chinese / Japanese entity names are fine, but folder names are kebab-case English. (See ORGANIZATION.md for the rationale.)

3. **Compute the destination path:**
   ```
   wiki/entities/<domain>/<type>/<slug>.md
   ```
   Where `<slug>` is the entity's display name (Chinese OK, spaces OK — Obsidian handles both).

4. **Check for collision:**
   - If a file with the same slug exists at the same path → **merge** (read existing, fold in new info, preserve frontmatter).
   - If a file with the same slug exists at a *different* `<domain>/<type>` → flag in log and ask the user which is correct (do not silently duplicate).

5. **Write the file** using `references/ENTITY_TEMPLATE.md`. Frontmatter MUST include:
   ```yaml
   ---
   domain: <kebab-case>
   type: <kebab-case>
   status: draft
   sources: [<raw filename or url>]
   created: <YYYY-MM-DD>
   ---
   ```

6. **Append a one-line entry to `wiki/log.md`:**
   ```
   YYYY-MM-DD HH:MM  ingest  +  finance/process/年度結算流程.md  (from raw/2026-04-27-meeting.md)
   ```

7. **Update `wiki/index.md`** (v1.3.2 — was implicit, now explicit):

   a. **Add the new entity links** under the appropriate H3 category section. If no fitting category exists, add a new H3 (or new H2 for a brand-new domain).

   b. **If a new `domain` was introduced**, append it to the header's "🏷 分類" line:
      ```
      🏷 分類：N domain（orders / claude / wiki / helpdesk / <new>）× M type（...）
      ```

   c. **Recompute and update the entity / map count** in the "📊 條目數" header line. Count via `find wiki/entities -name '*.md' | wc -l` (recursive — see [[Recursive Scan SOP]] in vault CLAUDE.md). Don't trust cached numbers.

   d. **Update the "📅 最後更新" header line** with today's date and a one-line summary of this ingest:
      ```
      📅 最後更新：2026-04-27（旅遊攝影團小程序 v1.3 ingest 完成）
      ```

   ⚠️ Skipping any of (a)-(d) leaves the index out of sync with reality — easily missed when the body changes look correct but the header counters lag.

8. **Track which entities came from this raw file.** Keep an in-memory list of (raw_path, [entity_paths_written]) — needed for the routing step below.

### After all entities are written from a raw file: Route the raw

For each raw file you just processed:

9. **Decide where the raw file goes.** Read `references/PARA_ROUTING.md` and follow its algorithm:
   a. List existing PARA structure (`10-Notes/`, `20-Projects/`, `30-Areas/`, `40-Resources/`, `50-Archive/`, `raw/09-ARCHIVE/`)
   b. Form a primary proposal (reuse-first; coin a new subfolder if needed — see Q3=A in PARA_ROUTING.md)
   c. Always offer the archive fallback: `raw/09-ARCHIVE/YYYY-MM/<filename>`
   d. Present both proposals to the user, wait for their reply (`1` / `2` / `archive` / `<custom path>` / `skip`)

10. **Move the raw file** to the chosen destination. Create folders as needed. Never silently overwrite.

11. **Update `sources:` in every entity that cites this raw.** Search across `wiki/entities/` for any entity whose frontmatter `sources:` lists the OLD raw path; rewrite those entries to the NEW path. (See PARA_ROUTING.md step 9.)

12. **Log the routing:**
    ```
    YYYY-MM-DD HH:MM  route  raw/2026-04-27-meeting.md → 20-Projects/2026-Q1-財務稽核/sources/  (3 entities updated)
    ```

### Mode B — Backfill (one-time, on user request)

Trigger: user says "整理現有 entities", "backfill", "把舊的 entities 也分類", or v1.3.0 is freshly installed and the user runs ingest for the first time.

Follow `references/MIGRATION.md` step by step. Summary:

1. Scan all `.md` files anywhere under `wiki/entities/` (including the flat root).
2. For each file: read frontmatter + content, infer `domain` + `type` (same rules as Mode A, reuse-first).
3. Produce a **dry-run plan** (a markdown table: current path → proposed path → reason).
4. Show the plan to the user. Wait for "go" / "execute" / "confirm".
5. On confirmation: add/update frontmatter, then move files. Do all moves atomically per-batch (per domain).
6. **Do NOT rewrite `[[wiki links]]`** — Obsidian resolves wiki links by basename, so moving a file does not break links pointing to it. Verify this by spot-checking 2-3 links after the move.

## Critical guarantees

- **Link preservation.** Obsidian's `[[Name]]` syntax resolves by filename, not path. Moving `entities/年度結算流程.md` → `entities/finance/process/年度結算流程.md` does not break any incoming `[[年度結算流程]]` link. This is the cornerstone that makes physical reorganization safe.

- **Slug stability.** Never rename the file's basename during organize/backfill. Only move it. Renaming would break links.

- **Idempotency.** Running ingest or backfill twice on the same input must produce the same tree. Don't append duplicate frontmatter, don't re-create existing entities, don't re-move already-correctly-placed files.

- **No silent merges across domains.** If the same entity name shows up under two different `<domain>/<type>` paths, surface it — never auto-merge across boundaries.

- **Reuse over invention.** When in doubt about whether to coin a new domain/type or reuse an existing one, reuse. Taxonomy entropy is the enemy.

- **`sources:` integrity.** Whenever a raw file moves (steps 9-10 above), every entity that cites it must be updated in the same operation. A broken `sources:` link is silent rot — the entity looks fine but its provenance is gone.

- **`raw/` root is an inbox.** After ingest finishes, no `.md` files should remain at `raw/` root. Each one is either routed to PARA, sent to `raw/09-ARCHIVE/YYYY-MM/`, or explicitly logged as "user said skip".

## After ingest

Tell the user:
- How many entities were created / updated / merged
- Any new `<domain>` or `<type>` folders that were introduced (so they know the taxonomy grew)
- Where each raw file ended up (PARA path or 09-ARCHIVE), and how many entities had `sources:` updated as a result
- Any collisions or ambiguities flagged for their attention
- A reminder to run `wiki-compile` if maps need to be regenerated

## References

- `references/ENTITY_TEMPLATE.md` — frontmatter schema and body structure
- `references/ORGANIZATION.md` — domain/type inference rules, slug normalization, taxonomy hygiene
- `references/PARA_ROUTING.md` — where raw source files go after ingest (PARA reuse-first, 09-ARCHIVE fallback, sources: update protocol)
- `references/MIGRATION.md` — step-by-step backfill procedure for existing flat entities
- `references/LINK_CONVERSION.md` — (existing) how raw refs become `[[wiki links]]`
