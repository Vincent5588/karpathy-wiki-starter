# MIGRATION.md — backfilling existing flat entities to v1.3.0

A one-time procedure for moving everything in `wiki/entities/*.md` into the new `wiki/entities/<domain>/<type>/` hierarchy. Triggered when:

- The user upgrades to plugin v1.3.0 and runs `wiki-ingest` for the first time, or
- The user explicitly says "backfill" / "整理現有 entities" / "把舊的也分類" / "migrate to v1.3.0".

## Safety contract

Before doing anything:

1. **No file is moved without a written-out plan first.** Always dry-run, show the plan, wait for confirmation.
2. **No basename is renamed.** Only paths change. (Renaming would break `[[wiki links]]`.)
3. **Idempotent.** Re-running this on an already-migrated tree is a no-op.
4. **Reversible per-batch.** Group moves by `domain` so the user can roll back one domain without unwinding everything.

## Procedure

### Phase 1 — Discovery

1. List every `.md` file under `wiki/entities/` (recursive). Include both the flat root and any pre-existing subfolders.

2. For each file, read its current frontmatter:
   - **Has `domain` AND `type` AND is at the matching path?** → Already correct, skip.
   - **Has `domain` AND `type` but path doesn't match?** → Schedule a move.
   - **Missing `domain` or `type`?** → Schedule classification + move.

3. Build a working list of every file that needs action.

### Phase 2 — Classification (for files missing frontmatter)

For each file in the working list that lacks `domain` / `type`:

1. Read the file's title (`# Heading` or filename) and body.
2. Apply the inference algorithm in `ORGANIZATION.md`:
   - Step 1: list existing folders to see the current taxonomy
   - Step 2: try to fit
   - Step 3-5: coin sparingly, normalize
3. Record the proposed `domain` and `type`.
4. If genuinely unable to classify → assign `_unsorted`.

### Phase 3 — Dry-run plan

Produce a markdown table and show it to the user. Sort by current path so the user can scan it.

```markdown
## Migration plan (dry run)

**X files to move, Y already correct, Z need user input.**

### New folders that will be created

- `wiki/entities/finance/process/`
- `wiki/entities/finance/artifact/`
- `wiki/entities/claude/concept/`
- ...

### Moves

| # | Current path | → New path | domain | type | Reason |
|---|---|---|---|---|---|
| 1 | `entities/年度結算流程.md` | `entities/finance/process/年度結算流程.md` | finance | process | inferred from title + body |
| 2 | `entities/上下文壓縮.md` | `entities/claude/concept/上下文壓縮.md` | claude | concept | inferred from body |
| 3 | `entities/報銷表單 PDF.md` | `entities/finance/artifact/報銷表單 PDF.md` | finance | artifact | "PDF" + finance domain |
| ... |

### Needs your input

| # | File | Why | Options |
|---|---|---|---|
| K | `entities/反面案例提示.md` | Could fit `finance/concept` or `claude/pattern` | (a) finance/concept (b) claude/pattern (c) other |
```

Wait for the user to type "go" / "execute" / "looks good" / explicit edits.

### Phase 4 — Execute

Once confirmed:

1. **Create folders first.** All target `<domain>/<type>` folders before any move.
2. **Move files in batches grouped by domain.** Print "moving 11 files into `finance/`..." then proceed. Smaller blast radius if anything goes wrong.
3. **For files that needed frontmatter:** edit-in-place to add `domain` / `type` / `status: stable` (since these are pre-existing, mature entities) BEFORE moving.
4. **Do NOT touch `[[wiki links]]` anywhere.** Obsidian resolves by basename — moves are link-safe.
5. **Append a migration entry to `wiki/log.md`:**
   ```
   YYYY-MM-DD HH:MM  migration v1.2.1→v1.3.0  moved=NN  classified=NN  unsorted=NN
   ```

### Phase 5 — Verification

After execution:

1. **Spot-check 3 random `[[wiki links]]`** in `wiki/maps/*.md` and confirm they still resolve (open the linked entity, confirm it opens).
2. **Run `find wiki/entities/ -maxdepth 1 -type f -name "*.md"`** — there should be zero `.md` files at the flat root after migration (anything left there is by design, e.g. an `_index.md`).
3. **Print summary to user:**
   ```
   Migration complete.
   - 23 entities classified and moved
   - 2 entities flagged as _unsorted (please review)
   - 0 collisions
   - 4 new domain folders created: finance, claude, orders, general
   - 7 new type folders created: process, concept, role, artifact, pattern, system, rule
   ```
4. **Suggest running `wiki-compile`** to regenerate maps that may want to take advantage of the new structure.

## Edge cases

### A file is already in a subfolder but the wrong one

Treat it like any other move. Only the path differs from frontmatter.

### A file has frontmatter but values aren't kebab-case (e.g. `domain: Finance`)

Normalize to `finance` AND check whether `entities/Finance/` and `entities/finance/` would collide. If both exist, merge into the lowercase one.

### Two files have the same basename in the flat root and one already in a subfolder

This was already a latent ambiguity. Surface to the user before doing anything — let them decide.

### `Templates/` or other non-entity files end up under entities/

If you find something that doesn't look like an entity (e.g. a template, a draft, an empty stub), report it but do not migrate it. Ask the user whether to move it elsewhere.

### Backfill is interrupted

Re-running the procedure is safe. Phase 1 will detect already-correct files and skip them; only the remainder gets re-planned.
