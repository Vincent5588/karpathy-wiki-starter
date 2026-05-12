---
title: "規則 H：stable artifact 改動必加版本歷程"
tags: ["claude-md-rule", "rule-H"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 H：stable artifact 改動必加版本歷程

任何 `status: stable` 的 artifact，每次有意義改動（≥ 3 行內容變動或新增章節）必須在檔案內維護 `## 0. 版本歷程` table：

```markdown
## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | YYYY-MM-DD | 初版建立 |
| v1.1 | YYYY-MM-DD | 主要變動描述 |
```

新版**倒序追加**（最新的在最下面）。

## 為什麼 frontmatter 的 `updated:` 不夠

| 信號 | 粒度 | 回答的問題 |
|------|------|-----------|
| frontmatter `updated: YYYY-MM-DD` | 粗 | 「最後改是哪天？」 |
| `## 0. 版本歷程` table | 細 | 「這次改了什麼？跟上一版差別在哪？」 |

兩者並存——`updated:` 給工具用，版本表給人腦用。

## 例外條款

- **draft / 短頁**（< 50 行、單一概念的 entity）不必加
- **artifact / 長 doc / 多次迭代的 stable entity** 必加
- 不確定要不要加 → 加。後悔加了 < 後悔沒加

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
