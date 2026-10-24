# ORGANIZATION.md

How to choose `domain` and `type` for a new entity, and how those values become folder paths. Read this before assigning either field.

## Goals

1. **Findability.** The user should be able to navigate `wiki/entities/` like a file system and locate any entity in 2-3 clicks.
2. **Stable taxonomy.** Folder names don't churn. Once `finance/` exists, every finance entity goes there — no `accounting/`, no `Finance/`, no `finance_stuff/`.
3. **Open vocabulary.** No fixed enum. The taxonomy grows as new subject areas appear, but it grows slowly and deliberately.
4. **Link safety.** Folder structure must never break `[[wiki links]]`. (Obsidian resolves by basename — moving files is safe as long as basenames don't collide.)

## The two fields

### `domain` — the subject area

Answers: *"What part of my world does this entity belong to?"*

Should be a noun, kebab-case, English ASCII, ideally one word. Examples that have appeared in this wiki:

- `finance` — anything related to 財務 / 報銷 / 帳目
- `claude` — Claude usage patterns, prompting, AI workflow
- `orders` — the order system (其全貌 already mapped)
- `general` — cross-cutting (use sparingly — usually a sign you should pick a more specific domain)

### `type` — the kind of thing

Answers: *"What category of object is this?"*

Should be a noun, kebab-case, English ASCII. Common types that recur:

| `type` | Meaning | Examples |
|---|---|---|
| `process` | A procedure / workflow / SOP | 年度結算流程, 報銷審核流程 |
| `concept` | An abstract idea or term | 上下文壓縮, 反饋循環 |
| `role` | A persona / responsibility | Finance Approver, 部門主管 |
| `artifact` | A concrete document, form, or output | 報銷表單 PDF, 月結報表 |
| `pattern` | A reusable approach or technique | 並行 Claude 實例, 四種使用模式 |
| `system` | A named system or subsystem | 公告系統, TodayPage |
| `rule` | A rule, policy, or constraint | 折扣上限, 金額精度 |

These are **suggestions, not a fixed list**. Coin a new `type` only when none of the existing ones fit cleanly.

## Inference algorithm

Follow these steps in order whenever you need to assign domain/type:

### Step 1 — List existing folders

Look at what's already in `wiki/entities/`. The current taxonomy is the source of truth.

### Step 2 — Try to fit into existing folders

For the entity at hand, ask: *"Which existing `<domain>/<type>` pair would I naturally look in to find this?"*

If a clean fit exists → **use it exactly** (same spelling, same casing).

### Step 3 — If no fit, identify which axis is missing

- New subject area? → coin a new `domain`, reuse an existing `type` if possible.
- New kind of object? → coin a new `type`, reuse an existing `domain` if possible.
- Both new? → pause and consider whether the entity is really atomic, or whether it should be split.

### Step 4 — Coin the new value carefully

When coining:
- **One word if possible.** `process` not `business-process`. `hr` not `human-resources`.
- **Lowercase kebab-case.** `claude-code` not `ClaudeCode` or `claude_code`.
- **Plural-neutral.** Use `process` (singular form), not `processes` — folder names read better as "kind of thing" labels.
- **Avoid abbreviations the future-you won't recognize.** `hr` is fine (universally understood); `cm` for "context management" is not.

### Step 5 — Sanity-check against synonyms

Before saving, search the existing taxonomy for synonyms:
- About to coin `procedure`? Already have `process`? → use `process`.
- About to coin `human-resources`? Already have `hr`? → use `hr`.
- About to coin `tool`? Already have `system`? → think hard about whether they're really different.

## Path computation

```
wiki/entities/<domain>/<type>/<basename>.md
```

- `<basename>` is the entity's display name. **Do not slugify Chinese.** Obsidian handles Chinese filenames and spaces fine.
- `<basename>` does NOT include `<domain>` or `<type>` — `wiki/entities/finance/process/年度結算流程.md`, not `wiki/entities/finance/process/finance-process-年度結算流程.md`.

### Special case — the `_unsorted/` bucket

If you genuinely cannot determine `domain` or `type` (e.g. the raw input is too vague), write the entity to:

```
wiki/entities/_unsorted/<basename>.md
```

with `domain: unsorted` and `type: unsorted`. Flag it in the ingest log so the user knows to triage it later. The leading underscore keeps it sorted to the top of the folder listing.

## Slug normalization for `domain` / `type`

Applied automatically before writing:

| Input | Normalized |
|---|---|
| `Finance` | `finance` |
| `Human Resources` | `human-resources` (but check Step 5 — `hr` likely exists) |
| `claude_code` | `claude-code` |
| `ProcessFlow` | `process-flow` |
| `行政` | (Chinese is rejected for folder names — pick an English equivalent like `admin`) |

## Collision rules

### Same basename, same path → merge

`wiki/entities/finance/process/年度結算流程.md` already exists, and ingest produces another `年度結算流程` for `finance/process`. → Read existing, fold in new content, preserve `created`, bump `updated`.

### Same basename, different `<domain>/<type>` → flag

`wiki/entities/finance/process/年度結算流程.md` exists, and ingest produces `年度結算流程` for `claude/concept`. → This is almost certainly an error. **Stop and ask the user** which is correct. Do NOT silently create both — Obsidian wiki links would become ambiguous.

### Same `<domain>/<type>`, near-duplicate basenames → flag

E.g. `年度結算流程` vs `年度結算-流程` vs `Year End Process`. → Surface as a possible duplicate; let the user decide whether to merge or rename.

## Taxonomy hygiene checklist

Run mentally before every ingest:

- [ ] Did I list existing folders before coining anything new?
- [ ] If I coined a new `domain` or `type`, can I justify why no existing one fit?
- [ ] Are my new values lowercase kebab-case ASCII?
- [ ] Did I check for synonym collisions?
- [ ] Will the resulting path look right when listed alongside existing entries?
