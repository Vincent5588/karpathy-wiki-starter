---
title: "規則 J：entity 必繁中 + 翻譯責任前移到產出階段"
tags: ["claude-md-rule", "rule-J"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 J：entity 必繁中 + 翻譯責任前移到產出階段

**核心原則**：vault 內全部 wiki entity / map / index 都用**繁體中文**。但**翻譯責任前移到 raw 產出階段**，不在 ingest 階段做逐字翻譯（70 KB 英文 raw 逐字翻吃 ~30K output tokens，成本不划算；NotebookLM 摘要品質已夠用）。

## 三條子規則

**J.1 — entity 必須全文繁中**：
- entity 標題、frontmatter `title`、章節標題、列點、表格——全部繁中
- 例外：純命令（`bash`）、程式碼片段、約定俗成不譯廠商名（GitHub / Google / API / MCP 等）

**J.2 — 英文專有名詞中英對照**（首次出現時）：
- 格式：`English（中文說明）` 或 `中文（English）`
- ✅ `Retrieval-Augmented Generation（檢索增強生成，RAG）`
- 後續重複使用可只用一種

**J.3 — 英文 / 外文 quote 加繁中翻譯**（強化規則 D）：
```markdown
> "Original English quote from the source."
>
> 繁中：「翻譯文字。」
```

## Raw 各語言的處置

| Raw 語言 | 處置 |
|---------|------|
| **繁體中文** | 直接 ingest 抽 entity |
| **英文（YT 影片）** | 走 youtube-to-notebooklm skill → NotebookLM 產**繁中摘要報告** → 從報告抽 entity |
| **英文（網頁文章）** | (a) 丟 NotebookLM 產繁中報告（推薦）、(b) 直接 Archive 不 ingest |
| **簡體中文** | ingest 時 LLM 順手簡轉繁 + 詞彙台灣化 |
| **日文 / 其他** | 比照英文走 NotebookLM 摘要報告路徑 |

## 反模式

- ❌ **手動翻譯大量英文 raw 後 ingest** → 太貴
- ❌ **抽 entity 時直接保留英文 / 簡中** → 違反 J.1
- ❌ **忘記 quote 翻譯** → 違反 D + J.3
- ❌ **過度翻譯專有名詞**（把 `MCP` 完全取代）→ 應保留原文 + 中英對照（J.2）

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
