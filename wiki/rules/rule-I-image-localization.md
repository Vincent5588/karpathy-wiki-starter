---
title: "規則 I：raw 含圖必下載到 Attachments + entity 本地引用"
tags: ["claude-md-rule", "rule-I"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 I：raw 含圖必下載到 Attachments + entity 本地引用

當 raw 檔含外部圖片（`![alt](https://...)` 形式）時，**ingest 流程必須下載圖片到本地 + entity 改用本地引用**，不准只引用外部 URL。

## 為什麼

| 風險 | 後果 |
|------|------|
| 外部 CDN 連結會壞 | 原作者刪文 / 換 domain → 圖永遠失效 |
| vault 不自包含 | 備份 / 搬家時得另外處理外部資源 |
| 離線使用 | 外部圖片無法在離線環境瀏覽 |

## 標準動作

1. 下載到 `Attachments/<source-basename>/<NN>-<short-desc>.<ext>`
2. entity 引用改本地：`![alt](Attachments/<source>/<NN>-<file>.jpg)`

## 執行模型

| 環境 | 能否直接下載 | 做法 |
|------|------------|------|
| **Claude Code session** | ✅ 可 | 直接 curl 下載 |
| **使用者本人** | ✅ 可 | 雙擊執行 LLM 產出的 download script |
| **Cowork / Claude.ai**（web-restricted）| ❌ 不可 | 產 `outputs/download_<source>.command` script |

## 例外條款

- **純裝飾圖**（網站 banner / footer logo）可省略
- **太大 / 版權敏感的圖**只放原檔連結 + 註明「原檔有圖」

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
