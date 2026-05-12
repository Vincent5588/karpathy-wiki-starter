---
title: "WIKI_TODO"
tags: [todo, wiki-work]
created: 2026-01-01
updated: 2026-01-01
status: stable
cssclasses: [wide]
---

# Wiki — 待辦清單

> 最後更新：YYYY-MM-DD
>
> **目前狀態**：**0 entities** / **0 maps** / Lint Score **—** / Plugin **v1.4.3** / vault patch **v1.0**

---

## 0. 上下文

> 在這裡寫下你使用這個 vault 的目標，例如：
> - 「記錄我的讀書筆記，建立個人知識庫」
> - 「整理工作上的 SOP 和系統知識」
> - 「累積 AI/LLM 相關學習筆記」

---

## 🔴 高優先

| 待辦 | 說明 | 預計工時 |
|------|------|---------|
| **第一次 ingest** | 把一篇文章 / 一份筆記丟進 `00-Inbox/`，執行 `ingest 00-Inbox/你的檔案.md` | ~30 min |
| **設定你的 domain** | 決定主題分類（如 work / learning / personal）| ~15 min |
| **跑第一次 lint** | 了解健康狀態 | ~5 min |

---

## 🟡 中優先

| 待辦 | 說明 | 預計工時 |
|------|------|---------|
| **建立第一個 map** | 在 `wiki/maps/` 建一個跨主題的 mermaid 地圖 | ~30 min |
| **設定 Web Clipper** | 依 [[Wiki_Web_Clipper_範本]] 設定 Obsidian Web Clipper 三個範本 | ~30 min |
| **自訂 CLAUDE.md §0** | 把版本歷程改成你自己的 | ~10 min |

---

## 🟢 低優先 / 長期

| 待辦 | 說明 |
|------|------|
| **補 §0 版本歷程** | 對 stable artifact 依規則 H 補版本歷程 |
| **建立 wiki/maps/ MOC** | 建跨主題地圖（需要 20+ entity 才有意義）|
| **評估 Quartz 部署** | 把 vault 發布成靜態網站（[[CLAUDE]] §10 規則 F/G 相關）|

---

## ✅ 已完成

### 2026-01-01（初始建立）

- [x] 從 karpathy-wiki-starter 模板建立 vault
- [x] 設定 CLAUDE.md、PROGRESS.md、index.md

---

## 📊 Lint 健康度進度

| 時點 | Score | Orphans | Missing | God nodes | Collisions |
|------|-------|---------|---------|-----------|------------|
| 初始（0 entity）| — | — | — | — | — |

---

## 🎮 觸發指令速查

| 想做 | 講 |
|------|---|
| 第一次 ingest | 「ingest 00-Inbox/你的檔案.md」 |
| 健康檢查 | 「lint wiki」 / 「巡一下 wiki」 |
| 修補問題 | 「批量修 wiki」 |
| 升 stable | 「批次升 stable」 |
| 建新 entity | 「我要建一個關於 X 的 entity」 |

---

← 回到 [[wiki/index]] | [[CLAUDE]] | [[wiki/PROGRESS]]
