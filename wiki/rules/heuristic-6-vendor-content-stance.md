---
title: "經驗法則 6 — 廠商 thought-leadership 內容 ingest → 立場標註"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-08-13
tags: [rule, heuristic, ingest, vendor, 立場標註, bias]
aliases: [heuristic-6, 骨架 vs 工具置入, vendor content stance]
---

# 經驗法則 6：廠商 thought-leadership 內容 ingest → 立場標註

> ingest **廠商 / 第一方 thought-leadership**（官方 playbook、白皮書、vendor 的「how to build X」ebook…）時，內容常**混合普適方法論與自家產品置入**。抽 entity 時必標立場，區分「**方法論骨架（普適）**」vs「**工具置入（廠商 specific）**」，否則未來引用會把「某產品的特定用法」誤當普適原則、污染知識庫。

## 適用觸發

| 信號 | 是否適用 |
|---|---|
| 來源是廠商官方 ebook / whitepaper / blog | ✅ 適用 |
| 內容夾帶「用我們的產品做 X」的導流 | ✅ 適用 |
| 中立第三方教材 / 論文 / 開源社群文 | ❌ 不必（無廠商立場）|
| 使用者自產內容 / 專案實測報告 | ❌ 不必 |

## How to apply

1. **錨點 / map entity 必加一條立場標註**（放 `## 待解 / 矛盾` 或獨立段）：
   > ⚠️ 本框架是 `<廠商>` 的 thought-leadership，帶產品置入；引用時請區分**方法論骨架（普適）** vs **工具置入（`<廠商>` specific）**。
2. **個別 entity 若本身重工具置入**（整條圍繞某產品功能），該 entity 的待解也補一句。
3. **內文寫法**：方法論骨架用中性語言（不綁廠商）；工具置入處**明確點名廠商**，讓讀者一眼分辨哪些可換工具、哪些是廠商限定。
4. **不擋 stable**：此類立場 caveat 屬經驗法則 5 的「**未來／立場型**」（非矛盾／存疑型）→ 不阻礙升 stable。

## 反模式

- ❌ 把廠商的「用我們產品做 X」原封抄成普適原則（未標立場）
- ❌ 每個 atomic entity 都塞冗長免責聲明——**錨點載一次**即可，個別 entity 只在重工具置入時補一句
- ❌ 因為「有 `## 待解` 立場標註」就把 entity 卡在 draft（違反經驗法則 5）

## 相關

- 經驗法則 5（`wiki/rules/heuristic-5-promote-refinement.md`）— 立場型待解不擋 stable
- 經驗法則 7（`wiki/rules/heuristic-7-transcript-verification.md`）— 常同時觸發：既要查證數字，也要標立場
- 規則 K（`wiki/rules/rule-K-raw-precheck.md`）— 預檢判定「廠商內容」時觸發本法則

---

← 回到 `CLAUDE.md` §10
