---
title: "Wiki PROGRESS — 新 Session 熱身"
tags: ["progress", "session-warmup"]
updated: YYYY-MM-DD
cssclasses: [wide]
---

# ⚡ Wiki PROGRESS — 新 Session 熱身

> **每次開新 Claude session 第一步讀此檔**。30 秒掌握當前狀態。
> 完整待辦 → `wiki/TODO.md`｜詳細異動 → `wiki/daily/`

---

## 📊 系統健康狀態

| 指標 | 狀態 | 備註 |
|------|------|------|
| Entity 總數 | **0** | 剛建立，尚無 entity |
| Lint Score | **—** | 尚未跑過 lint |
| Draft 比例 | **—** | — |
| Plugin 版本 | **v1.4.3** | 8 skills |
| Vault patch | **v1.0** | 初始模板 |

---

## 🎯 當前最高優先（Top 5）

> 剛建立的 vault，建議從以下開始：

| # | 待辦 | 觸發指令 |
|---|------|---------|
| 1 | **第一次 ingest** — 把一篇文章丟進 00-Inbox/，執行 ingest | `ingest 00-Inbox/你的檔案.md` |
| 2 | **設定你的 domain** — 決定你的主題分類（work / learning / personal…）| 告訴 Claude「我想建立 X domain」 |
| 3 | **跑第一次 lint** — 看健康狀態 | `巡一下 wiki` |
| 4 | **自訂 CLAUDE.md §0** — 把版本歷程改成你自己的 | 手動編輯 |
| 5 | **建立你的第一個 daily** — 開始紀錄 | `wiki/daily/YYYY/MM/YYYY-MM-DD.md` |

---

## 📝 上次 Session 摘要

**YYYY-MM-DD**（初始建立）

- 從 karpathy-wiki-starter 模板建立 vault
- 尚未 ingest 任何內容

---

## 📋 維護規則

- **開 session**：讀此檔（30 秒），確認健康狀態 + 當前 top 優先
- **結束 session**：更新「上次 Session 摘要」（1-3 行 bullet）+ 視需要調整 Top 5 排序
