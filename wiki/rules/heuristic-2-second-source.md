---
title: "經驗法則 2：同主題第 2 篇 raw → 補 source 而非建新 entity"
tags: ["claude-md-rule", "heuristic-2"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 經驗法則 2：同主題第 2 篇 raw → 補 source 而非建新 entity

當不同 raw 描述**同一個主題、同一個概念**，且既有 entity 已存在（特別是 stable 狀態）時：

✅ **正確動作**：把新 raw 路徑加進既有 entity 的 `source:` 列表，bump `updated`
❌ **錯誤動作**：建一個「概念 v2」之類的新 entity（重複 = 違反 reuse-first）

## 為什麼

- **多 source 增強可信度**：1 個 source 可能誤讀，2 個獨立 source 同方向 = 高可信度
- **避免分裂**：建 v2 後 wiki-link 指向不明、backlink 也分裂
- **Compounding**：每次新 raw 來都補強既有，不從零再建

## 判斷流程

```
1. 跑 wiki-query 看既有 entity 有沒有覆蓋這主題
2. 有 ≥ 70% 重疊 → 補 source（本法則）
3. 有 < 70% 重疊但有新 atomic 概念 → 抽新概念建 entity，舊 source 仍補進相關既有 entity
4. 完全新主題 → 標準 ingest 流程
```

## 例外：何時該建新 entity

- 新 raw 提了**既有沒寫的 atomic 概念**
- 不同**主流 / 流派 / 時代**的同主題
- 同主題但**從不同角度切入**

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
