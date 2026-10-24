# PARA_ROUTING.md

How to route a raw source file to its final resting place after `wiki-ingest` extracts entities from it. Mirrors the reuse-first philosophy of `ORGANIZATION.md` (which handles wiki taxonomy), but applied to the user's PARA structure.

## When this applies

After Mode A ingest finishes writing all entities from a raw file, before reporting completion to the user. Each raw file gets one routing decision (regardless of how many entities it spawned).

Mode B (backfill) does NOT trigger routing — there's no raw file involved.

## Two destinations

Every raw file ends up in exactly one of these two places:

1. **A specific PARA path** — when the content has a clear home (project, area, or resource).
2. **`raw/09-ARCHIVE/YYYY-MM/`** — when the user opts out of PARA classification, or the content has no clear PARA fit.

`raw/` itself is treated as an inbox: nothing should remain at the `raw/` root after ingest finishes.

## Algorithm

### Step 1 — List existing PARA structure

Before proposing anything, scan one level deep into each PARA tier the user has:

```
10-Notes/
  daily/
  meeting/
20-Projects/
  2026-Q1-財務稽核/
  Cowork-研究/
30-Areas/
  財務/
  Claude-Workflow/
40-Resources/
  PDF-規範/
  文章/
50-Archive/
  ...
raw/
  09-ARCHIVE/
    2026-04/
    2026-03/
```

This is the live taxonomy. Every proposal must either reuse an existing folder or coin a new one with the same naming style.

### Step 2 — Read raw content + entities just written

Use both signals to decide where the raw file belongs:
- **Raw content** — what is this document about?
- **Entities extracted** — what `domain` did they end up in? (e.g. all entities went to `finance/` → strong signal this raw is finance-related)

### Step 3 — Form a primary proposal (reuse-first)

Try to fit into existing PARA subfolders, in this priority order:

1. **Project match** — does the content reference an active project that already has a `20-Projects/<name>/` folder? → Propose `20-Projects/<name>/sources/<filename>`.
2. **Area match** — is this an ongoing-responsibility topic with an existing `30-Areas/<name>/`? → Propose `30-Areas/<name>/sources/<filename>`.
3. **Resource match** — is this reference material for an existing `40-Resources/<topic>/`? → Propose `40-Resources/<topic>/<filename>`.
4. **Note match** — is this a meeting note, daily log, or fleeting note that fits an existing `10-Notes/<subtype>/`? → Propose `10-Notes/<subtype>/<filename>`.

If a match is found → that's proposal (1).

### Step 4 — When no existing folder fits → coin one (per user setting Q3=A)

If no existing PARA subfolder fits cleanly:

1. Decide which PARA tier is correct (Project / Area / Resource / Note).
2. Coin a new subfolder name. Naming style must match what's already there:
   - Look at sibling folder names in that tier (e.g. `2026-Q1-財務稽核` uses `YYYY-Q#-中文` pattern → follow it for new projects)
   - Default to Chinese if existing siblings are Chinese
   - Match the case/punctuation conventions in use
3. Propose the new folder as proposal (1), explicitly marked `(create new folder)`.

The user can still reject this in their reply — they're not committed to creation just because it was proposed.

### Step 5 — Form proposal (2): the archive fallback

Always offer the no-PARA-decision exit:

```
raw/09-ARCHIVE/YYYY-MM/<filename>
```

Where `YYYY-MM` is derived from the raw file's date (frontmatter date if present, else file mtime, else today).

### Step 6 — Present to the user

Format:

```
RAW: raw/2026-04-27-meeting.md
Entities extracted: 3 (all → finance/)

Suggested destinations:
  (1) 20-Projects/2026-Q1-財務稽核/sources/2026-04-27-meeting.md
      reason: extracted entities live in finance/, project name "財務稽核" appears in content header
  (2) raw/09-ARCHIVE/2026-04/2026-04-27-meeting.md
      reason: archive fallback

Reply: 1 / 2 / archive / <your-own-path>
```

When proposal (1) requires creating a new folder, mark it explicitly:

```
RAW: raw/2026-04-28-orders-spec.md
Entities extracted: 5 (all → orders/)

Suggested destinations:
  (1) 30-Areas/訂單系統-運維/sources/2026-04-28-orders-spec.md   ← (create new folder)
      reason: no existing PARA folder for order-system ongoing work; entities are orders/system
  (2) raw/09-ARCHIVE/2026-04/2026-04-28-orders-spec.md
      reason: archive fallback

Reply: 1 / 2 / archive / <your-own-path>
```

### Step 7 — Parse user response

Accept these reply forms:

| Reply | Action |
|---|---|
| `1` / `go` / `accept` / `好` | Use proposal (1). Create new folder if marked. |
| `2` / `archive` / `歸檔` | Move to `raw/09-ARCHIVE/YYYY-MM/`. |
| `<any path string>` | Use that exact path as the destination. Create folders as needed. |
| `skip` / `leave` | Don't move the raw file. Log a warning so the user knows raw/ root has leftovers. |

When in doubt about the reply, ask once for clarification rather than guessing.

### Step 8 — Move the raw file

1. Create destination folder if it doesn't exist.
2. Move file (preserve original filename).
3. If a file with the same name already exists at destination → append `-2`, `-3`, etc. before the extension. Do NOT silently overwrite.

### Step 9 — Update `sources:` in every affected entity

Critical step — without this, the wiki entities will have broken `sources:` links.

For every entity written from this raw file (you tracked these in Mode A step 5):

1. Read the entity's frontmatter `sources:` list.
2. Find the entry matching the OLD raw path.
3. Replace with the NEW raw path.
4. Save the entity.

Example:
```yaml
# before
sources:
  - raw/2026-04-27-meeting.md
  - https://example.com/spec

# after
sources:
  - 20-Projects/2026-Q1-財務稽核/sources/2026-04-27-meeting.md
  - https://example.com/spec
```

Do this for ALL entities pointing at this raw, not just the ones created in this ingest run. (An old entity might already cite the same raw file.) Use grep / search across `wiki/entities/` to find them all.

### Step 10 — Log the routing

Append to `wiki/log.md`:
```
YYYY-MM-DD HH:MM  route  raw/2026-04-27-meeting.md → 20-Projects/2026-Q1-財務稽核/sources/  (3 entities updated)
```

## Multi-file ingest

If the user ingests several raw files in one go:

- Process them sequentially. For each one: extract entities, then run this routing protocol.
- Don't batch routing decisions ("here are 5 raw files, where should each go?") — the user will lose track. One file at a time, one decision at a time.
- Exception: if 3+ raw files are obviously the same project (e.g. all named `2026-04-27-meeting-part1.md`, `-part2.md`, etc.), bundle them into one decision: "these 3 files all → same destination?"

## Anti-patterns (don't do these)

- ❌ **Silently moving a raw file to PARA** without asking. Routing is always user-confirmed (except when their reply was already collected).
- ❌ **Dropping the raw file in `raw/09-ARCHIVE/` root** instead of `YYYY-MM/`. Always include the year-month subfolder.
- ❌ **Leaving raw at `raw/` root after ingest finishes**. Either move it (PARA or archive), or explicitly log "user said skip — raw still at root".
- ❌ **Forgetting to update `sources:`**. Broken citations are silent failures — the entity looks fine but its provenance link is dead.
- ❌ **Renaming the raw file during the move**. Keep the basename. (Same reasoning as wiki entities — basenames are stable identifiers.)
- ❌ **Auto-creating top-level PARA folders** like `20-Projects/`. Only create *subfolders* under tiers the user already has. If `20-Projects/` doesn't exist, use the archive fallback and ask the user to set up PARA properly.

## Examples of good routing decisions

### Example 1 — Clear project match
```
RAW: raw/2026-04-27-q1-audit-meeting.md
content mentions "Q1 稽核專案" repeatedly, action items for the team

Existing: 20-Projects/2026-Q1-財務稽核/

Proposal (1): 20-Projects/2026-Q1-財務稽核/sources/2026-04-27-q1-audit-meeting.md
```

### Example 2 — Ongoing area, new subfolder needed
```
RAW: raw/2026-04-28-orders-architecture.md
content describes order system internals, ongoing reference material

Existing: 30-Areas/財務/, 30-Areas/Claude-Workflow/  (no 訂單系統)

Proposal (1): 30-Areas/訂單系統-運維/sources/2026-04-28-orders-architecture.md  (create new folder)
  — naming follows sibling style "中文-中文"
```

### Example 3 — Genuine archive case
```
RAW: raw/2026-04-25-misc-thoughts.md
content is a brain-dump of unrelated ideas, no project or area fit

Proposal (1): 10-Notes/daily/2026-04-25-misc-thoughts.md
Proposal (2): raw/09-ARCHIVE/2026-04/2026-04-25-misc-thoughts.md  (likely the right call)
```

### Example 4 — Multiple entity domains in one raw
```
RAW: raw/2026-04-26-cross-team-sync.md
Entities extracted: 6 — 4 went to finance/, 2 went to claude/

Proposal (1): 30-Areas/財務/sources/2026-04-26-cross-team-sync.md
  reason: dominant entity domain is finance/ (4 of 6); claude/ entities are tangential
Proposal (2): raw/09-ARCHIVE/2026-04/2026-04-26-cross-team-sync.md

(Don't try to split a raw file across two PARA folders — pick the dominant home.)
```
