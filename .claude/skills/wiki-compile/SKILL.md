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
3. **Cite source**: each entity's frontmatter `source` array must include the original document path
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

### Phase 4: Update wiki/index.md

Add a new section for the topic with all new entities listed by sub-category.

### Phase 5: Update wiki/log.md

Append:

```
| YYYY-MM-DD | Compile | source/path | N entities + 1 map | Topic name; phases A/B/C/D |
```

### Phase 6: Auto-archive the source（v1.1 新增）

成功完成 Phase 1-5 後，**把 raw/ 來源檔搬到 raw/09-archive/**：

```bash
mkdir -p raw/09-archive
mv "raw/{path}/{file}" "raw/09-archive/$(date +%Y%m%d)_{file}"
```

**規則**：
- ❌ 絕對不要 Read raw/09-archive/ 下的檔案
- ❌ 絕對不要用 archive 內檔案再次 compile
- 報告中要明示「✓ 已歸檔到 raw/09-archive/YYYYMMDD_{file}」
- 來源若是 40-Resources/ （已組織的長期資料）而非 raw/ → **不歸檔**，因為非 inbox

### Phase 7: Report

Summarize:
- Total entities created (by phase)
- Map page created
- Top hub entities (most cross-linked)
- Source archived to: raw/09-archive/YYYYMMDD_{file}（如適用）
- Suggested next compile target

## Rules

- **Always confirm the plan before writing.** Compiling 20+ entities is heavy — get user buy-in first.
- **Phases let user catch problems early.** If phase 1 has wrong scope, fix before phase 2-4.
- **Source field is mandatory.** Every entity must trace back to its origin section.
- **Map is required.** Compiling without a map leaves entities adrift.
- **Always archive the raw/ source** after success (Phase 6). Skip if source is in 40-Resources/.
- **Never read or re-compile** files in raw/09-archive/.

## See also

- `references/COMPILATION_PHASES.md` — phase planning examples
- `references/MAP_TEMPLATE.md` — mermaid map structure with examples
