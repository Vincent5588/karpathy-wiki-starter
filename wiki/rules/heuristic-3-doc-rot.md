---
title: "經驗法則 3：「文件即真理」失效要回查 source"
tags: ["claude-md-rule", "heuristic-3"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
---

# 經驗法則 3：「文件即真理」失效要回查 source

當文件寫的解法跟實際行為不符時，**不要只信文件，要直接讀 source / config / build output**。文件腐化（doc-vs-code drift）是必然的，紀錄正確 ≠ 系統正確。

## 觸發條件

- 「文件寫對但行為錯」≥ 2 次同類事件 → **一定是 drift**
- 「應該觸發某 side effect 但沒觸發」也是 drift 信號（quiet failure = silent drift）
- 「上次踩過的雷又來了」→ 需在 source 加 inline `# NOTE:` 指向文件章節

## 必查的三層 source

1. **實際執行結果**：跑一次看輸出，不要只讀文件
2. **鎖定版本的 source**：看你實際用的版本，不是 HEAD
3. **實際跑的指令 / config**：看 yaml / script 裡實際的 command，不是看部署紀錄

## 預防 SOP

(a) 每個重要 config / script 段落加 inline `# NOTE:` 指向文件章節
(b) 定期排「diff actual config vs doc」找出新冒出來的 drift
(c) 寫文件時不只記「正確答案」，**也記「曾經踩到的反例」**

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 從 CLAUDE.md §10 拆出，同步自 Vincent5588 v1.3.36 |
