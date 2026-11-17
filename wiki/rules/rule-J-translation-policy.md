---
title: "規則 J：entity 必繁中 + 翻譯責任前移到產出階段"
tags: ["claude-md-rule", "rule-J"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-11-17
---

# 規則 J：entity 必繁中 + 翻譯責任前移到產出階段

**核心原則**：vault 內全部 wiki entity / map / index 都用**繁體中文**。但**翻譯責任前移到 raw 產出階段**，不在 ingest 階段做逐字翻譯（70 KB 英文 raw 逐字翻吃 ~30K output tokens，成本不划算；先產繁中報告、再從報告抽 entity 即可）。

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
| **英文（YT 影片）** | **單支**走本機 fast-path（yt-dlp 抓字幕，沒字幕才本機轉錄）直接產繁中報告（[[heuristic-4-yt-fastpath\|經驗法則 4]]）；**多支跨來源**才走 youtube-to-notebooklm（NotebookLM）→ 從報告抽 entity |
| **英文（網頁文章）** | 照 [[rule-K-raw-precheck\|規則 K]] §K.2 先產繁中報告（附查證表）再 ingest；或直接歸檔不 ingest |
| **簡體中文** | ingest 時 LLM 順手簡轉繁 + 詞彙台灣化 |
| **日文 / 其他** | 比照英文（影片同上；網頁照規則 K §K.2） |

## 反模式

- ❌ **手動翻譯大量英文 raw 後 ingest** → 太貴
- ❌ **抽 entity 時直接保留英文 / 簡中** → 違反 J.1
- ❌ **忘記 quote 翻譯** → 違反 D + J.3
- ❌ **過度翻譯專有名詞**（把 `MCP` 完全取代）→ 應保留原文 + 中英對照（J.2）

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.1 | 2026-11-17 | 英文 YT 影片單支改走本機 fast-path、多支才走 NotebookLM（對齊經驗法則 4）；英文網頁改照規則 K §K.2 前處理（附查證表）。同步自 Vincent5588 規則 J v1.1 與規則 K v2 |
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
