# Ingest Audit Report Template

每次 wiki-ingest 成功後寫一份到 `wiki/reports/INGEST_YYYYMMDD_HHmm.md`。

## 完整模板

```markdown
---
title: "Ingest Report YYYY-MM-DD HH:mm"
type: audit
source: "[[raw/{path}/{file}]]"
created: YYYY-MM-DD
---

# 📊 Ingest Audit Report

> Source: raw/{path}/{file}
> 處理時間：YYYY-MM-DD HH:MM
> 工具：wiki-ingest v1.2

## 1. 處理摘要

| 項目 | 數量 |
|------|------|
| 新建 entities | N |
| 更新 entities（加 backlink） | M |
| 衝突標記 | C |
| 強連結 | S 條 |
| 推斷連結 | I 條 |
| 推斷比例 | X%（建議 < 40%） |

## 2. 🆕 新建頁

- [[A]] — 一句概念描述
- [[B]] — 一句概念描述

## 3. 🔄 更新頁

- [[X]] — 加了 N 條 backlink（指向 [[A]], [[B]]）
- [[Y]] — 加了 1 條 backlink + 衝突標記

## 4. ⚠️ 衝突（如有）

- [[C]] vs raw 原文：對 X 的說法不一致
  - 既有頁說：...
  - raw 原文說：...
  - 兩邊都加了 ⚠️ callout，待人工釐清

## 5. 🌉 意外連結（cross-cluster）

raw 同時連到的不同主題群集（從 wiki/index.md 的分類判斷）：

- [[訂單系統全貌]] 群 + [[Claude 4.6 全景]] 群 → 之前不太相連
- 暗示概念可能是橋樑，值得在後續寫一篇連通文

## 6. 💡 建議下一步

- [[D]] 在原文有提但**沒新建頁**，要 ingest 嗎？
- raw/01-articles/ 還有 N 份未處理檔案
- 推斷連結比例偏高（X%），建議跑 `wiki-lint` 看看是否該升級為強連結

## 7. 📈 Hub 變動

主要 hub 頁的 inlinks 在這次 ingest 後的變化：

| 頁面 | Before | After | Δ |
|------|--------|-------|---|
| [[PricingService]] | 14 | 16 | +2 |
| [[Cowork]] | 9 | 10 | +1 |

## 8. 🔗 完整新增連結

對審計用，列出所有這次新加的 [[link]]：

### 強連結
- 在 [[A]]：[[訂單審核流程]]、[[折扣規則]]
- 在 [[B]]：[[Hooks]]

### 推斷連結
- 在 [[A]]：[[PricingService]] ??
- 在 [[X]] backlink：[[A]] ??

← 回到 [[wiki/index|wiki/]]
```

## 命名

- 路徑：`wiki/reports/INGEST_YYYYMMDD_HHmm.md`
- 範例：`wiki/reports/INGEST_20260426_1432.md`
- 同一天多次 ingest 用時分區別

## 為什麼要這份 report

1. **回饋密度**：log.md 一行不夠看，audit 是給「事後檢視」用的
2. **意外連結偵測**：跨群集連結是高價值訊號（你過去沒想到的關聯）
3. **連結品質追蹤**：推斷比例如果一直高，代表原文與既有 wiki 不太相關，或 LLM 過度發揮
4. **下一步引導**：CANDIDATE_NEW 沒被建頁的概念可以排隊
