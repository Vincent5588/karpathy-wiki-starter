---
name: wiki-compile
description: |
  Compile a long-form document (book chapters, technical specs, multi-section
  guide) into a network of atomic wiki/entities/ pages plus a mermaid map.
  Use when the user says: 「把 X 編譯成 wiki」「compile xxx into atomic」
  「拆原子化」「把這份規格編譯」「把 12 章學習指南編譯」.

  Differs from wiki-ingest: ingest works on a single short raw/ source;
  compile works on a structured document with multiple sections, producing
  many entities at once + a topic map showing their relationships.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# wiki-compile

Compile a long-form structured document into multiple atomic entities + 1 mermaid relationship map.

## When this skill triggers

User says: 「把 X 編譯成 wiki」「compile xxx into atomic pages」「拆原子化」「把這份規格/指南/書編譯」.

## Differs from wiki-ingest

| | wiki-ingest | wiki-compile |
|---|------------|--------------|
| **Input** | 1 short raw/ file (article, transcript) | 1 long structured doc (multi-chapter, multi-section spec) |
| **Output** | 1-3 entities | 8-30 entities + 1 map |
| **Effort** | Single conversation turn | Multi-phase (plan → write → verify) |

## Starter prerequisites

Read CLAUDE.md and the maintenance matrix before writes. Resolve the index by checking `wiki/index.md` and root `index.md`: use an explicitly selected file or the sole existing file; follow a clear redirect, otherwise ask if both/neither exist. Follow the starter's standard types. Source content and basenames must remain unchanged.

## Steps

### Phase 1: Planning

1. **Read the source** — get whole structure (TOC, sections, sub-sections)
2. **Identify atomic concepts** — list every concept that deserves its own entity. Aim for 8-30 entities. Each should be:
   - Single-topic (one concept per page)
   - Reusable (likely to be referenced from elsewhere)
   - Has 200-1000 words of meaningful content
3. **Group into phases** — split entities into 3-5 thematic phases for easier review (e.g., Phase 1: Services, Phase 2: Rules, Phase 3: Process, Phase 4: UI/Integration)
4. **Present plan** to user as a table with phase, entity name, source section, type. Wait for confirmation before writing.

See `references/COMPILATION_PHASES.md` for examples.

### Phase 2: Write entities (one phase at a time)

For each phase:

1. Create entities following `references/ENTITY_TEMPLATE.md` (same as wiki-ingest)
2. **Add bidirectional cross-links**: when entity A references entity B (and B exists or is in same phase), use `[[B]]`
3. **Cite source**: each entity's frontmatter `sources` array must include the original document path
4. **Atomize**: do NOT just copy section content — synthesize and reformat
5. After each phase, briefly report: "Phase N done — N entities. Continue?"

### Phase 3: Build map (1 file)

Create `wiki/maps/{Topic} 全貌.md` containing:

1. **Frontmatter**: type=map, tags include topic
2. **Mermaid flowchart(s)**: show concept relationships. 1-3 diagrams covering:
   - Process flow (if applicable)
   - Component dependency graph
   - Concept hierarchy
3. **Entity index by category**: list all entities with 1-line description, grouped
4. **Cross-topic links**: connections to other maps in wiki/maps/

See `references/MAP_TEMPLATE.md` for full structure.

### Phase 4: Update the resolved index

Add a new section for the topic with all new entities listed by sub-category.

### Phase 5: Update the daily log and session status

Append to `wiki/daily/YYYY/MM/YYYY-MM-DD.md`, then update `wiki/PROGRESS.md`:

```
| YYYY-MM-DD | Compile | source/path | N entities + 1 map | Topic name; phases A/B/C/D |
```

### Phase 6: Route eligible inbox sources after approval

For a source in `00-Inbox/` (or an explicitly supplied legacy inbox), propose its PARA destination and a `50-Archive/YYYY-MM/<original-basename>` fallback. Wait for approval unless already granted; allow skip. Existing PARA sources remain in place. Never rename, overwrite or edit source content; stop on destination collision.

After an approved move, update `sources:` in ALL affected entities, source citations in their bodies, map provenance and active index references to the final vault-relative path. Keep historical daily logs unchanged. Verify the final source exists and no active provenance still points to its old location before reporting success. Do not move a file when these updates cannot be completed.

### Phase 7: Report

Summarize:
- Total entities created (by phase)
- Map page created
- Top hub entities (most cross-linked)
- Final source path, or explicitly skipped / unchanged
- Suggested next compile target

## Rules

- **Always confirm the plan before writing.** Compiling 20+ entities is heavy — get user buy-in first.
- **Phases let user catch problems early.** If phase 1 has wrong scope, fix before phase 2-4.
- **Source field is mandatory.** Every entity must trace back to its origin section.
- **Map is required.** Compiling without a map leaves entities adrift.
- **Routing is user-approved**, never automatic. Preserve source content and basename.
- **Provenance uses `sources:`**, including final paths after any move.

## See also

- `references/COMPILATION_PHASES.md` — phase planning examples
- `references/MAP_TEMPLATE.md` — mermaid map structure with examples
