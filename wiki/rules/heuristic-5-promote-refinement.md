---
title: "經驗法則 5 — promote 判斷精煉（待解分型 + owner 共審）"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-08-13
tags: [rule, heuristic, promote, status, stable, draft]
aliases: [heuristic-5, 待解兩型, owner 共審升 stable]
---

# 經驗法則 5：promote 判斷精煉

> 跑 `wiki-status-promote` 時，兩條精煉 default 判斷的規律。來源：一次批次升 stable 的實作歸納——3 個含待解、2 個當天才建的 entity 照樣該升 stable，證明現行 default 太保守。

## 精煉 1：`## 待解` 要分兩型

skill 的 default 把「含 `## 待解 / 矛盾` 區塊」一律歸 🟡 留 draft——**太粗**。待解分兩型：

| 型 | 特徵 | 對 promote |
|---|---|---|
| **未來 / 取決於** | 「Phase N 才需要」「參數待補」「值待實測」——內容沒錯，只是還沒展開 | ✅ **不擋 stable**（保留待解區塊即可）|
| **矛盾 / 存疑** | 「與 X 衝突」「此處可能錯」「兩說不一」——內容本身待裁決 | 🟡 **強制留 draft**，直到裁決 |

→ 判斷時讀待解的**內容**，不是只看「有沒有 `## 待解`」。

## 精煉 2：同 session owner 逐輪共審 → 可直接升 stable

- 這是 `status` 鐵則「**stable = trust marker，不是 mtime**」的延伸：entity 雖然是當天 `created`，但**若 owner 在本 session 逐輪審過**（改錯、加內容、定結構）＝ 人類審查已經成立 → **不必等 30 天**即可升 stable。
- 反面同樣成立：LLM 自建但 owner **沒**過目的 entity，放 30 天也**不該**自動升——trust 未建立，**age 不等於 trust**。

## How to apply

跑 promote 時：

1. 對每個含待解的 candidate，讀待解型別 → 未來型照升、矛盾型留 draft。
2. 今天建、但 owner 本 session 審過的，列 🟢 並註明「owner 共審」。
3. 仍照規則 E（show before write），owner 最終拍板。

## 相關

- `wiki-status-promote` skill — 本法則精煉其分類邏輯
- 經驗法則 1（`wiki/rules/heuristic-1-batch-ingest.md`）— 同源整批審（另一條 promote 加速）
- 經驗法則 6（`wiki/rules/heuristic-6-vendor-content-stance.md`）— 立場型待解同樣不擋 stable

---

← 回到 `CLAUDE.md` §10
