---
title: "經驗法則 1：同源 ingest 整批一起審"
tags: ["claude-md-rule", "heuristic-1"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 經驗法則 1：同源 ingest 整批一起審

當一份 raw 文件 ingest 出 N 個 entity，其中**一個 entity 升 stable**，**其他 N-1 個應一次性審查整批升 stable**——它們的可信度根源於同一個業務確認過的 source，沒理由分散處理。

實踐：跑 wiki-status-promote 時，看到某 domain 有任一個 stable 的 entity，自動推薦該 domain 內**所有同 source 的 draft** 一起進入候選清單。

## 為什麼

- **可信度共源**：同一份文件 / 同一個業務裁決確認過的 source，抽出的每個 entity 可信度相同
- **避免碎片化審查**：一個 entity 今天審、另一個下個月審，容易造成同源 entity 狀態不一致

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
