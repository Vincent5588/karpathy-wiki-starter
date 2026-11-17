---
title: "規則 I：raw 含圖必下載到 Attachments + entity 本地引用"
tags: ["claude-md-rule", "rule-I"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-11-17
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

1. 下載到 `Attachments/<分類>/<source-basename>/<NN>-<short-desc>.<ext>`
   - **分類**＝主題或專案，名稱跟 `40-Resources/` 的分類同一套（例如 `learning`、`work`、某個專案名）；用過的分類就沿用，不開同義詞
   - 🔴 **不要在 `Attachments/` 根層開新資料夾或平鋪檔案**——根層只放 README 與分類夾，平鋪的檔案＝待分類
2. entity 引用改本地：`![alt](Attachments/<分類>/<source>/<NN>-<file>.jpg)`；路徑含空白或全形括號時改用 `![[檔名]]`（`![](…)` 寫法 Obsidian 不認得這種路徑）
3. 搬既有附件一律**在 Obsidian 裡搬**（檔案列表拖曳或右鍵移動），連結才會自動改；frontmatter 字串與行內 code 裡的路徑 Obsidian 不會改，要另外搜尋改

## 執行模型

| 環境 | 能否直接下載 | 做法 |
|------|------------|------|
| **Claude Code session** | ✅ 可 | 直接 curl 下載 |
| **使用者本人** | ✅ 可 | 雙擊執行 LLM 產出的 download script |
| **Cowork、對話分頁、Claude.ai**（不能連外下載時）| ❌ 不可 | 產 `outputs/download_<source>.command` script 給使用者執行 |

## 例外條款

- **純裝飾圖**（網站 banner / footer logo）可省略
- **太大 / 版權敏感的圖**只放原檔連結 + 註明「原檔有圖」
- **既有附件不另開搬遷工程**：新下載的照新規則放；舊的改到時再順手搬

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.1 | 2026-11-17 | 路徑多一層分類 `Attachments/<分類>/<source>/`（分類與 40-Resources 同一套）；加「根層不開新夾」、空白路徑改 `![[…]]`、在 Obsidian 裡搬三條。同步自 Vincent5588 規則 I v1.1 |
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
