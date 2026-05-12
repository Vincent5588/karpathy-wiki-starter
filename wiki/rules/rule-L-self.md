---
title: "規則 L：未來新規則 / 經驗法則直接拆檔"
tags: ["claude-md-rule", "rule-L"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 L：未來新規則 / 經驗法則直接拆檔

**核心原則**：CLAUDE.md 主檔有上限。**未來新規則 / 經驗法則 / 大型補充直接寫 `wiki/rules/rule-X.md`，主檔只留 1-row 速查 + 連結**。

## 觸發條件（符合任一條件就拆）

- **內容超過 30 行**（含 markdown 表格、code block、case 範例）
- **跨多個 sub-section**（有「鐵則 / 例外 / 為什麼 / 跟其他規則關係 / 觸發條件」分節）
- **含長 case study**
- **預期會持續擴充**

## 主檔 1-row 速查格式

```markdown
### 規則 X：xxx（vY.Z）

> 一行核心鐵則。詳細：`wiki/rules/rule-X.md`。

**Why**：一行原因。**How to apply**：一行觸發條件。
```

## 拆檔 frontmatter 規格

```yaml
---
title: "規則 X：xxx"
tags: ["claude-md-rule", "rule-X"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## 例外（永遠 inline 的）

- 規則 A / B / C（三大鐵則）
- ⚡ Quick Reference 表

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36（本規則自我示範）|
