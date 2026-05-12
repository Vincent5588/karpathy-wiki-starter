---
title: "規則 E：寫檔前先提案（show before write）"
tags: ["claude-md-rule", "rule-E"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 E：寫檔前先提案（show before write）

> **對檔案系統的任何寫入動作必須先在對話中讓使用者看 → 確認 → 才動手。**

## 必須先提案的動作

- 建立新 entity / map / daily / log（**新檔**）
- 大規模改 entity 內容（譬如重寫一個 entity 主體）
- 移動 / 改名檔案
- 改 frontmatter 結構（type、domain、status 等）
- 批次操作（譬如 wiki-repair 一次改 N 個檔）
- 寫 plugin / skill / 工具腳本

## 不需要先提案的動作

- 純讀取（Read / Glob / Grep）
- bash 查詢類（`ls` / `find` / `wc -l`）
- 跑 `wiki-lint` / `wiki-query` 等唯讀 skill
- 顯示計算結果

## 提案的格式

```
我要做：[動作描述]
影響檔案：[路徑列表]
變動內容（節錄）：
   ...

確認後執行？
```

短任務（單檔小編輯）可省略格式，但**必須在動手前在訊息中描述清楚**。

## 為什麼這條規則重要

(a) **不可逆成本**：AI 寫錯後刪檔 / 重整 / 改連結每一步都是隱性成本
(b) **使用者校正方向**：reviewing draft 是 vault 品質的 last mile（沒這步 LLM 容易腦補）
(c) **養成 LLM 自我約束**：寫進規則後，LLM 自己會先停下來想「這要不要提案」

## 例外條款

- 使用者明確說「直接改」「不要再問」「OK 照做」 → 後續 ≤30 分鐘內可省略提案
- 使用者批准了一個多步驟計畫 → 步驟內的每個動作不必再個別提案
- 但**新建檔案 / 改 vault CLAUDE.md** 永遠要提案，不論前面同意過什麼

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
