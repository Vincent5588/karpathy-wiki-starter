---
title: "Wiki 健康度監控"
tags: [monitoring, lint, health, vault-meta]
domain: wiki
type: monitoring
status: draft
maintained_by: LLM
created: 2026-01-01
updated: 2026-01-01
cssclasses: [wide]
---

# 🩺 Wiki 健康度監控

> Lint score 趨勢紀錄。每次跑完 `lint` 由 LLM 追加一 row。配 [[Wiki_儀表板]] 看快照、配 [[WIKI_TODO]] 排修補。
>
> ⚠️ **空樣板**：使用者第一次跑 `lint wiki` 後，LLM 依本檔骨架追加首筆紀錄。

---

## 📈 Lint Score 趨勢

| 時點 | Score | Orphans | Missing | God nodes | Collisions | 觸發事件 |
|------|-------|---------|---------|-----------|------------|---------|
| — | — | — | — | — | — | 初始 |

---

## 🎯 健康度判讀

| Score | 評等 | 行動 |
|-------|-----|------|
| 90-100 | 🟢 健康 | 維持節奏 |
| 70-89 | 🟡 注意 | 排 1-2 個修補進 [[WIKI_TODO]] |
| 50-69 | 🟠 警告 | 跑 `wiki-repair --plan-only` 規劃批次修 |
| <50 | 🔴 危急 | 暫停新 ingest，先修現有 |

---

## 🔧 常見問題類型 vs 修補 skill

| 問題 | 修補手段 |
|------|---------|
| 孤兒頁（orphan）| 加 backlink 或併入相關 entity |
| Missing reference | 補 stub entity 或修 wikilink |
| God node | 拆檔（依規則 L 模式）|
| Collision（同 basename）| 改 basename 加區分詞（依 §8 衝突處理）|
| Source 路徑壞掉 | 修 frontmatter `source:` |
| Draft 比例 > 30% | 跑 wiki-status-promote |

---

## 📝 維護紀律

- 每次 `lint` 跑完 → 追加一 row（規則：[[Wiki_維護觸發規則]] §2）
- score 跌 ≥ 10 → 在 [[WIKI_TODO]] 開高優先修補項
- 連續 3 次同類問題沒修 → 提案 root cause 分析（譬如「為何 orphan 一直長」）

---

## 相關

- [[Wiki_儀表板]] — 快照面板
- [[Wiki_維護觸發規則]] §2 — Lint cascade 規則
- [[WIKI_TODO]] — 修補待辦

← 回到 [[wiki/index]]
