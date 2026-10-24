# ENTITY_TEMPLATE.md

The canonical shape of a wiki entity file. v1.3.0 adds **`domain`** and **`type`** as required frontmatter — these drive the folder routing.

## File location

```
wiki/entities/<domain>/<type>/<entity-name>.md
```

The basename of the file is the entity's display name (Chinese OK, spaces OK). Folder segments are kebab-case ASCII.

## Frontmatter (required)

```yaml
---
domain: <kebab-case>          # required — see ORGANIZATION.md
type: <kebab-case>            # required — see ORGANIZATION.md
status: draft | stable | deprecated
sources:                       # where this entity came from
  - raw/2026-04-27-meeting.md
  - https://example.com/spec
created: 2026-04-27
updated: 2026-04-27            # bump on every meaningful edit
aliases:                       # optional — alternate names this entity is known by
  - 年度結算
  - year-end close
---
```

### Field semantics

| Field | Required | Notes |
|---|---|---|
| `domain` | yes | The subject area this entity belongs to. Examples that have appeared: `finance`, `claude`, `orders`, `general`. New domains are coined sparingly — see ORGANIZATION.md. |
| `type` | yes | The kind of thing this entity is. Examples: `process`, `concept`, `role`, `artifact`, `pattern`, `system`, `rule`. Reuse existing types whenever they fit. |
| `status` | yes | `draft` for fresh ingest, `stable` once reviewed, `deprecated` when superseded. |
| `sources` | yes | Provenance. At least one entry. **Auto-updated when raw files are routed**: if the source raw file moves from `raw/foo.md` to `20-Projects/X/sources/foo.md`, the `sources:` entry is rewritten in lockstep. See `PARA_ROUTING.md`. |
| `created` | yes | ISO date of first ingest. Never changes. |
| `updated` | yes on edit | ISO date of last meaningful change. |
| `aliases` | optional | Alternate display names. Useful for matching across languages. |

## Body structure

```markdown
# <Display Name>

> One-sentence definition. What is this thing, in plain language?

## 為什麼存在 / Why it exists

The problem this entity addresses, or the reason it was added to the wiki.

## 核心內容 / Body

The substantive content. Headings as needed. Wiki-link liberally to related entities: [[相關概念]].

## 關聯 / Relations

- **父層 / parent**: [[更廣的概念]]
- **子層 / children**: [[更具體的子項]]
- **相關 / related**: [[平行概念]]

## 來源 / Sources

- 原始筆記：`raw/<file>`，第 N 段
- 補充：[link]
```

## Worked examples

### Example 1 — Finance process

File path: `wiki/entities/finance/process/年度結算流程.md`

```yaml
---
domain: finance
type: process
status: stable
sources:
  - raw/2026-04-15-finance-handbook.md
created: 2026-04-15
updated: 2026-04-27
aliases:
  - 年度結算
  - year-end settlement
---

# 年度結算流程

> 財務每年度針對全公司帳目做結算與回寫的標準作業流程。

## 為什麼存在
...
```

### Example 2 — Claude concept

File path: `wiki/entities/claude/concept/上下文壓縮.md`

```yaml
---
domain: claude
type: concept
status: draft
sources:
  - raw/2026-04-26-claude-notes.md
created: 2026-04-26
---

# 上下文壓縮

> 在長對話中將早期訊息摘要化以節省 token 的技巧。
...
```

### Example 3 — System component

File path: `wiki/entities/orders/system/公告系統.md`

```yaml
---
domain: orders
type: system
status: stable
sources:
  - raw/2026-04-20-orders-overview.md
created: 2026-04-20
---

# 公告系統
...
```

## Anti-patterns (do NOT do these)

- ❌ `domain: Finance` — must be lowercase kebab-case
- ❌ `domain: accounting` if `finance` already exists — reuse
- ❌ `type: finance-process` — `domain` and `type` are orthogonal; the domain doesn't go in the type
- ❌ Inventing `type: process-v2` — bump `status` or version inside the body, not the type
- ❌ Two entities with the same basename in different `<domain>/<type>` folders — Obsidian wiki links will become ambiguous. If you genuinely need both, give them distinguishing names.
