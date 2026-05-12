---
title: "規則 K：raw 預檢 SOP"
tags: ["claude-md-rule", "rule-K"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 K：raw 預檢 SOP

**核心原則**：wiki-ingest（或 LLM 收到「ingest XXX」指令）**步驟 0 必須先偵測 raw 性質**，依類型路由到對應前處理 skill，不要假設 raw「已經是可 ingest 狀態」。

> ⚡ **快路徑**：raw 是用 Obsidian Web Clipper 抓進來的話，frontmatter 已自帶 `pending_action` 線索 → 直接讀該欄位即知該做什麼。

## Step 0 預檢分流表

| Raw 內容 | 偵測規則 | 自動提案 |
|---------|---------|---------|
| **frontmatter `pending_action: youtube-skill`** | Web Clipper YouTube 範本 | 直接 chain youtube-to-notebooklm |
| **frontmatter `pending_action: rule-K-precheck`** | Web Clipper Default 範本 | 看 `language` / `word_count` / `type` 走下方分流表 |
| **frontmatter `atomize: false`** 或 **路徑含 `longform/`** | longform | 建 1 個 entity（不拆），詳見 §3.1.1 |
| **裸 YT URL** | 檔長 < 300 bytes + match URL | 「先跑 youtube-to-notebooklm skill？」|
| **裸非 YT URL** | 檔長 < 300 bytes + non-YT URL | 「先用工具抓內容？或丟 NotebookLM？」|
| **大量英文文章** | 檔長 > 5 KB + 英文 char ratio ≥ 0.3 | 「丟 NotebookLM 摘要？或直接 50-Archive？」|
| **簡中文章** | 含「数据 / 软件 / 这个」 | 「ingest 時順手簡轉繁 + 詞彙台灣化」|
| **繁中 + 結構完整** | 預設 | **直接 ingest**（標準流程）|
| **空檔 / 只有 frontmatter** | body < 50 bytes | 「raw 內容不足，無法 ingest。要刪嗎？」|

## 決策樹

```
使用者：「ingest 00-Inbox/X.md」
  ↓
LLM 讀檔前 100 行（step 0 預檢）：
  ├─ 偵測檔長、URL pattern、語言比例、結構完整度
  ├─ 對照規則 K 分流表
  └─ 提案處理路線（規則 E）
       ↓
使用者批准：
  ├─ 「OK」→ 走標準 wiki-ingest 流程
  ├─ 「先跑 X skill」→ chain skill → 等產出後再 ingest
  └─ 「Archive」→ 移到 50-Archive，不 ingest
```

## 例外

- 使用者明確說「就是要從這檔直接抽 entity 不要前處理」→ skip 預檢
- raw 是混合型（前半繁中筆記 + 後半英文引用）→ 預設走標準 ingest
- 使用者已批准的 chain skill 流程內部步驟，不必每步再 step 0 預檢

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
