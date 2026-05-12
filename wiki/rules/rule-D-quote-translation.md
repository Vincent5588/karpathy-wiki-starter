---
title: "規則 D：英文 quote 必加繁中翻譯"
tags: ["claude-md-rule", "rule-D"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 規則 D：英文 quote 必加繁中翻譯

引用任何英文原文 quote 時，**必須**在原文 quote 下方緊接著一條繁中翻譯。格式：

```markdown
> "Original English text from the source."
>
> 繁中：「翻譯。」
```

## 範例（標準寫法）

```markdown
> "The wiki is a persistent, compounding artifact."
>
> 繁中：「Wiki 是一個持久且不斷複利的產物。」
```

## 規則細節

1. **兩條 quote 用空白 `>` 分隔**——讀起來像「原文 → 翻譯」的對照組
2. 翻譯前綴用「**繁中：**」三字 + 全形冒號，方便視覺辨識
3. 翻譯本身用「**「」**」全形雙引號包起來
4. 短句（< 10 詞）也要翻——別偷懶
5. 專有名詞 / 技術名詞**可保留英文，但須加繁中說明**（格式：`Term（中文說明）`，同規則 J.2）
6. 若原文有 **粗體** 強調，翻譯也要對應加粗
7. 多句長 quote 維持原文段落結構，翻譯也分段對應

## 不適用情境

- code block 裡的英文（`npm run build` 不翻）
- 標題、書名（直接引用即可）

## 為什麼這條規則重要

(a) 繁中為主的 vault 裡，英文 quote 不翻會破壞閱讀流暢度
(b) 翻譯本身是再次理解的過程，**強迫 LLM 不只是複製貼上原文**
(c) 未來查詢 / 跨檔搜尋時，繁中關鍵字也找得到原文意思

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
