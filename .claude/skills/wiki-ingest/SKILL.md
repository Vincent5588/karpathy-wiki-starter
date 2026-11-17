---
name: wiki-ingest
description: |
  Extract atomic entities from raw notes and write them into a hierarchical
  wiki/entities/[domain]/[type]/ structure. Use when the user says
  「ingest」「process raw」「extract entities」, or requests processing content in 00-Inbox/.
  Also handles backfill of existing flat entities.

  v1.3: entity 自動推論 domain/type 落到資料夾；raw 檔 ingest 完搬去
  PARA 子路徑或 50-Archive/YYYY-MM/，並改寫所有 entity 的 sources:。
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# wiki-ingest (starter v1.4.7)

> **v1.4.7（2026-11-17）**：加 Step 0.1 規則 K v2 預檢——Web Clipper 的 YouTube／GitHub 剪報、英文或被截斷的網頁先做報告（附查證表）再 ingest；被 `supersedes:` 取代的原剪報不 ingest；查證表「查無」的名稱不寫進 entity 正文。對齊維護者 wiki-ingest v1.3.4–v1.3.5 的通用部分。

Extract atomic concepts from raw, messy input and write them as well-formed wiki entities — **automatically classified into a domain/type folder hierarchy** so `entities/` never becomes a flat dumping ground.

## Starter conventions

- `00-Inbox/` is the source inbox. Accept an explicitly supplied legacy `raw/` path, but do not create a second inbox.
- Resolve the index using the wiki-query rule: inspect `wiki/index.md` and root `index.md`; use the sole existing file, follow an explicit redirect, or ask when ambiguous/missing. This starter ships root `index.md`.
- Read the vault's `CLAUDE.md` and `Wiki操作文件/Wiki_維護觸發規則.md` before proposing writes. Follow its type vocabulary (concept/process/system/pattern/rule/artifact/role/person) and atomize precheck; do not override it with generic examples below.
- Keep source content and basenames unchanged. Existing PARA sources are read-only and stay in place unless the user explicitly approves moving them.

## Inputs

- One or more files in `00-Inbox/` (or content the user pastes into the chat)
- Existing `wiki/entities/` tree (used to keep taxonomy consistent — reuse existing domain/type folder names whenever they fit)

## Outputs

- One `.md` file per atomic entity at `wiki/entities/<domain>/<type>/<slug>.md`
- Each file follows `references/ENTITY_TEMPLATE.md`
- An entry in today's daily `wiki/daily/YYYY/MM/YYYY-MM-DD.md` (step 6; required by `CLAUDE.md` §3.1 step 7)

## Pipeline

### Step 0: Show the starter maintenance plan

Before writing, cite `Wiki操作文件/Wiki_維護觸發規則.md` §1 and show the actual paths affected:

1. New or updated entities; any required map.
2. The resolved index: links, domain entries, counts and last-updated date.
3. `wiki/daily/YYYY/MM/YYYY-MM-DD.md` and session summary in `wiki/PROGRESS.md`.
4. Proposed inbox routing and all affected `sources:` references, only after approval.
5. Optional existing TODO, terminology and dashboard pages when relevant.

Wait for approval unless this scope is already authorized. Do not require or create a personal `Wiki_主目錄` or ingest-history hub. Do not invent missing maintenance pages; report the gap and propose a solution. For `atomize:false`, create one entity using a standard type, with the wrapper required by CLAUDE.md.

### Step 0.1: Rule K v2 precheck (before reading for entities)

Rule: `wiki/rules/rule-K-raw-precheck.md` (vault `CLAUDE.md` §10 規則 K). Read the raw's frontmatter **and full text** — the language ratio and truncation often only show further down — then:

| 情況 | 動作 |
|---|---|
| 另一份檔的 `supersedes:` 指到這份 raw | **不 ingest**；照規則 K §K.4 歸檔 |
| `pending_action: youtube-skill`、`github-skill`，或英文／被截斷的網頁剪報、裸網址 | **不從原剪報抽 entity**——先照規則 K §K.2 產報告／評估（附 §K.3 查證表，另存新檔、`supersedes:` 指回原剪報；YouTube 用 youtube-to-notebooklm 的報告格式），再 ingest 產出檔；GitHub 評估不 ingest，只落地到 `40-Resources/GitHub/` |
| 網址已出現在 `40-Resources/` 或既有 entity 的 `source` | 不重做，回報「已收過：<既有檔>」並提案歸檔原剪報 |
| 繁中且完整 | 往下走 Mode A |

🔴 **查證表的用法**：ingest 前處理產出時，entity 正文只用查證表 `正確` 或 `更正` 後的名稱；**`查無` 的名稱不寫進正文**，只放 `## 待解` 並標「查無」。使用者明確說「不要前處理、直接抽」時可跳過前處理，**查證不豁免**。

### Mode A — Standard ingest (default)

For each chunk of raw input:

1. **Identify entities after the atomize precheck.** For atomic input, use one reusable concept per entity; preserve an approved atomize:false source as one entity.

2. **For each entity, decide `domain` and `type` BEFORE writing:**

   a. **Read `references/ORGANIZATION.md`** for the inference rules (kebab-case, reuse-first; vault standard types take precedence).

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

6. **Append an entry to `wiki/daily/YYYY/MM/YYYY-MM-DD.md`:**
   ```
   YYYY-MM-DD HH:MM  ingest  +  finance/process/年度結算流程.md  (from raw/2026-04-27-meeting.md)
   ```

7. **Update the resolved index** (v1.3.2 — was implicit, now explicit):

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
   a. List existing PARA structure (`10-Notes/`, `20-Projects/`, `30-Areas/`, `40-Resources/`, `50-Archive/`)
   b. Form a primary proposal (reuse-first; coin a new subfolder if needed — see Q3=A in PARA_ROUTING.md)
   c. Always offer the archive fallback: `50-Archive/YYYY-MM/<filename>`
   d. Present both proposals to the user, wait for their reply (`1` / `2` / `archive` / `<custom path>` / `skip`)

10. **Move the raw file** to the chosen destination. Create folders as needed. Never silently overwrite.

11. **Update `sources:` in every entity that cites this raw.** Search across `wiki/entities/` for any entity whose frontmatter `sources:` lists the OLD raw path; rewrite those entries to the NEW path. (See PARA_ROUTING.md step 9.)

12. **Log the routing:**
    ```
    YYYY-MM-DD HH:MM  route  raw/2026-04-27-meeting.md → 20-Projects/2026-Q1-財務稽核/參考資料/  (3 entities updated)
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

- **`00-Inbox/` is the inbox.** Route only approved source files; personal longform and explicit skips may remain. Each one is either routed to PARA, sent to `50-Archive/YYYY-MM/`, or explicitly logged as "user said skip".

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
