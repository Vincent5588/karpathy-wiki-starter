# Compilation Phase Planning

## Why phases?

Compiling 20+ entities at once = high error rate, hard to review. Splitting into 3-5 phases lets the user verify after each batch.

## Example: Compiling a 12-chapter Claude learning guide

| Phase | Entities | Source sections | Type |
|-------|---------|-----------------|------|
| 1: Models & Products | 5 | Ch 1-2 | product |
| 2: Prompting | 7 | Ch 3-4 | technique |
| 3: Cowork + Code Implementation | 5 | Ch 5, 9 | concept |
| 4: Skill / MCP / Agent Advanced | 6 | Ch 10-12 | concept |
| Map | 1 | All | map |

**Why this split**:
- Phase 1 = orientation (foundational)
- Phase 2 = horizontal skills (prompting techniques)
- Phase 3 = practical implementation
- Phase 4 = advanced building blocks

User reviews after each phase. If phase 1 names feel wrong, fix before continuing.

## Example: Compiling a software spec (訂單系統規格)

| Phase | Entities | Type |
|-------|---------|------|
| 1: Core services | 8 | service |
| 2: Rules & Calculation | 8 | concept (rule) |
| 3: Process flows | 8 | process |
| 4: UI & Integration | 4 | concept (ui) |
| Map | 1 | map |

## Anti-patterns

❌ "Phase 1: chapters 1-3, Phase 2: chapters 4-6..." — purely structural, doesn't reflect concept clustering. Cluster by **topic**, not source order.

❌ "Phase 1: 30 entities" — too big. Cap at 8-10 per phase.

❌ "Phase 1: 1 entity" — too small. Combine into thematic phases of 4+.

## How to identify atomic concepts

Pass through the source 3 times:

1. **First pass**: list every concept name mentioned. Don't filter yet.
2. **Second pass**: cluster synonyms ("Few-shot prompting" + "1-shot example" + "範例提示" → 1 concept)
3. **Third pass**: filter by reusability. A concept that's only mentioned once and has no internal usefulness doesn't deserve its own page.

## When NOT to compile

If the source is a personal narrative (book chapter telling a story, podcast transcript), it's better to **wiki-ingest** (1 entity summary) than wiki-compile (force atomization that fights the genre).

Compile is for: specs, learning guides, structured technical docs, multi-concept reference material.
