---
title: "Wiki 儀表板"
tags: [dashboard, vault-meta, monitoring]
domain: wiki
type: dashboard
status: draft
maintained_by: LLM
created: 2026-01-01
updated: 2026-01-01
cssclasses: [wide]
---

# 📊 Wiki 儀表板

> 開 vault 第一眼看的 status pane。一頁掌握 vault 是否「活著」+ 近期動態。
>
> ⚠️ **空樣板**：使用者第一次跟 LLM 說「初始化儀表板」或「巡 wiki」時，LLM 依本檔骨架填入實際數據。

---

## 🟢 健康狀態快照

> 最後更新：YYYY-MM-DD

| 指標 | 當前值 | 上次 | 趨勢 |
|------|-------|------|------|
| Entity 總數 | — | — | — |
| Map 總數 | — | — | — |
| Lint Score | — | — | — |
| Draft 比例 | — | — | — |
| Orphan 數 | — | — | — |

---

## 🔥 近期動態（近 7 天）

| 日期 | 動作 | 摘要 |
|------|------|------|
| — | — | — |

---

## 📌 進行中重點

> 列 Top 3 進行中的 domain / project / 主題。詳細待辦見 [[WIKI_TODO]]。

- —

---

## 🗂 各 Domain 速覽

```dataview
TABLE WITHOUT ID domain AS "Domain", length(rows) AS "Entity 數"
FROM "wiki/entities"
GROUP BY domain
SORT length(rows) DESC
```

---

## 🆕 最近更新 10 個 entity

```dataview
TABLE WITHOUT ID file.link AS "頁面", domain AS "Domain", type AS "Type", updated AS "最後更新"
FROM "wiki/entities"
SORT updated DESC
LIMIT 10
```

---

## ⚠️ 待審 draft（前 10）

```dataview
LIST
FROM "wiki/entities"
WHERE status = "draft"
SORT updated DESC
LIMIT 10
```

---

## 相關

- [[Wiki_健康度監控]] — Lint score 趨勢
- [[WIKI_TODO]] — 完整待辦清單
- [[wiki/PROGRESS]] — 新 session 必讀狀態面板
- [[wiki/index]] — 主目錄

← 回到 [[wiki/index]]
