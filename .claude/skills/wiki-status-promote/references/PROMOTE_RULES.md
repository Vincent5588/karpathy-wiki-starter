# PROMOTE_RULES — 決策邏輯詳細規則

> 本檔給 wiki-status-promote skill 用。給每個 draft 候選打分後分類成 🟢 / 🟡 / 🔴。

## 信號權重（每個 entity 算分後決定分類）

### 加分信號（傾向升 stable）

| 信號 | +分 |
|------|------|
| `length(file.inlinks) ≥ 3` | +3 |
| `length(file.inlinks) ∈ [1, 2]` | +2 |
| `created` 距今 ≥ 90 天 | +2 |
| `created` 距今 ∈ [30, 90) 天 | +1 |
| `updated` 跟 `created` 不同（有迭代過） | +1 |
| 內容字數 ≥ 500 | +2 |
| 內容字數 ∈ [200, 500) | +1 |
| 有「## 相關概念」段含 ≥ 3 條 wiki-link | +1 |
| 有 frontmatter 完整 (domain / type / source / created / updated) | +1 |

### 扣分信號（傾向留 draft 或 deprecate）

| 信號 | -分 |
|------|------|
| 含 `## 待解` / `## 矛盾` / `## TODO` 區塊 | -5（強制 🟡） |
| 含 `⚠️` emoji 在 H2 標題或開頭 | -3 |
| `length(file.inlinks) == 0` | -2 |
| 內容字數 < 200 | -3 |
| `created` 距今 < 7 天 | -10（強制跳過，太新） |
| frontmatter 缺 `source:` 或 `domain:` | -2 |
| basename 跨 domain 衝突（lint 報告） | -10（強制 🟡，先解衝突） |

## 分類門檻

| 總分 | 分類 | 動作 |
|------|------|------|
| ≥ 5 | 🟢 stable | 提案升 stable |
| 0–4 | 🟡 keep draft | 留 draft + 加 review_by 90 天 |
| < 0 | 🔴 deprecate | 提案改 deprecated（除非有人類明顯保留意願） |

## 強制例外（覆蓋分數）

某些 entity 類型分數計算不準，要硬規則：

### 規則類 entity（`type: rule`）

業務規則類常常 inlinks 少（只在某 1-2 處被引用）但極為重要。**規則 entity 不適用 inlinks 加分機制**——只看內容完整度與年齡：

```
if type == "rule" and word_count >= 200 and age_days >= 30:
    score = max(score, 5)  # 強制至少 🟢 候選
```

### 人物類 entity（`type: person`）

人物頁通常都該升 stable（不太需要「驗證」），除非內容空白：

```
if type == "person" and word_count >= 300:
    score = max(score, 5)
```

### Hub 類 entity（被 ≥ 5 個 entity 引用）

Hub 是 vault 重要節點，不該還停留在 draft：

```
if length(file.inlinks) >= 5:
    score = max(score, 7)  # 強制建議 🟢
```

### 含 v1.X 註記的 entity

如 frontmatter 或內文標 `version: 1.0` 並有清楚 release date，視為已驗證：

```
if has_explicit_version_tag:
    score = max(score, 5)
```

## 升 deprecated 的細節

不是只改 status——還要在 entity 主體加：

```markdown
## ⚠️ Deprecated（YYYY-MM-DD）

**原因**：[單薄 / 跟某 entity 重複 / 已過時]

**替代 entity**（如有）：[[XYZ]]

**保留此頁的原因**：[歷史 reference / 維持 backlink 不斷]
```

如果這個 entity 沒有任何 inlinks 且 deprecated，下次 lint 會提示是否乾脆刪除（**deprecate 不等於 delete**——deprecate 是「不要再用、但保留歷史」）。

## review_by 的細節

留 draft 但加提醒：

```yaml
---
status: draft
review_by: YYYY-MM-DD  # 90 天後的日期
review_reason: "等補 backlink" / "等業務裁決待解問題" / "等 source ingest"
---
```

`wiki-lint` 跑時若看到 `review_by < today` → 提醒到期未審。

## 不同 mode 的 threshold 微調

| Mode | 🟢 門檻 | 說明 |
|------|--------|------|
| Quick | ≥ 6（嚴） | 只升非常確定的 |
| Triage | ≥ 5（標準） | 平衡 |
| Full | 不分類，全部逐筆人工決定 | 最慢、最徹底 |

## 跟 wiki-lint 的整合

如果使用者說「lint 完幫我升 stable」，先讀 `wiki/reports/LINT_*.md`，跳過：

- 被 lint 標 god-node 的 entity（要先處理）
- 被 lint 標 collision 的 entity
- 被 lint 標 inferred-link-heavy 的 entity（內容品質可能不夠）

剩下的才走本流程。
