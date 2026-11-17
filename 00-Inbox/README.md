---
title: "00-Inbox — 所有新素材的入口"
type: artifact
status: active
tags: [inbox, readme]
created: 2026-05-11  # 依 git 第一次加入的日期
updated: 2026-11-17
---

# 00-Inbox — 所有新素材的入口

> 這是你唯一需要主動使用的資料夾。

## 使用方式

把任何東西丟進來：
- 截圖、文章、PDF
- 會議筆記
- 讀書摘要
- 靈感、想法
- YouTube 影片連結

然後告訴 Claude：`ingest 00-Inbox/你的檔案.md`

## 注意

- ✅ **可以**：把檔案丟進來、讓 Claude 讀
- ❌ **不要**：手動整理這個資料夾的結構——讓 Claude 幫你路由
- ❌ **不要**：重新命名已有的檔案——檔名是穩定識別碼
- 💡 用 Web Clipper 剪的影片、GitHub 專案、英文或被截斷的網頁：AI 會先另做一份 `_報告`（附查證表）再整理，原剪報做完報告就收進 `50-Archive/`（規則 K）

## Daily/ 子資料夾

`00-Inbox/Daily/` 放你的每日個人筆記，使用 `40-Resources/Templates/Personal Daily.md` 模板。  
這些不會被 ingest 到 wiki，是你的私人記事本。

## longform/ 子資料夾

`00-Inbox/longform/` 放**想保留完整、不想被拆 atomic** 的素材（個人心得 / 旅遊紀錄 / 完整書評等）。

LLM ingest 時看到路徑含 `longform/` → 預設 `atomize: false`：
- ❌ 不拆 atomic entity
- ✅ 仍做 PARA 路由 + 寫 daily log

詳見 [longform/README.md](longform/README.md) 或 `40-Resources/Templates/Longform Note.md`。
