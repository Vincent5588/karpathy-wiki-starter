---
title: "Wiki 刪檔處理 SOP"
tags: [sop, deletion, archive, vault-meta]
domain: wiki
type: process
status: draft
maintained_by: LLM
created: 2026-01-01
updated: 2026-01-01
cssclasses: [wide]
---

# 🗑 Wiki 刪檔處理 SOP

> 三層緩衝期：**Active → 50-Archive → Delete**。任何「想刪」念頭都不直接 `rm`，先 archive 觀察 30 天。
>
> ⚠️ **空樣板**：使用者第一次說「刪掉 X」/「不要這個了」時，LLM 依本檔骨架走流程，並把首次刪檔紀錄填入下方追蹤表。

---

## 🚦 三層緩衝期

```
Active（10-Notes / 20-Projects / 30-Areas / 40-Resources / wiki/entities）
    ↓ Step 1：移到 50-Archive（保留歷史，留 redirect stub）
50-Archive/<原路徑>
    ↓ Step 2：30 天觀察期（沒人查、沒被引用）
    ↓ Step 3：人類批准才真刪（git rm，git history 仍可回溯）
真正刪除（極少數）
```

---

## 📋 操作步驟

### Step 1：Archive（任何時間都可做）

1. **show 計畫**：LLM 告知「我要把 X 移到 50-Archive/<路徑>，原位置留 redirect stub。確認？」（規則 E）
2. 等使用者批准
3. 移檔到 50-Archive
4. 原位置留 redirect stub（frontmatter `moved_to: [[新路徑]]` + 內文一句話）
5. 在當日 daily 加紀錄

### Step 2：30 天觀察期

- 期間若有 query / backlink 觸發 → **不刪**，可能還在用
- 期間沒任何 access → 進 Step 3 候選

### Step 3：真刪（git rm）

1. LLM 列「30 天無 access 的 archive 候選」清單
2. 使用者逐項批准（**不准批次自動刪**）
3. `git rm <檔>`，commit message 寫清楚刪除依據
4. 在當日 daily 加紀錄（含「為何刪」）

---

## ❌ 永遠不做的事

- ❌ 直接 `rm` 不走 Archive
- ❌ 跳過 30 天觀察期
- ❌ 批次自動刪（必須逐項人類批准）
- ❌ 刪 inbox 內容（規則 A：00-Inbox/ 唯讀）
- ❌ 刪有 backlink 的 entity（會斷既有引用）

---

## 📊 刪檔追蹤表

| 日期 | 檔案 | 動作 | 進入 archive 日 | 真刪日 | 依據 |
|------|------|------|---------------|--------|------|
| — | — | — | — | — | — |

---

## 🎯 何時 archive vs 何時直接刪

| 場景 | 處置 |
|------|------|
| stable entity 過時 | Archive（保留歷史 + backlink）|
| draft entity 確認沒用 | Archive |
| raw 已 ingest 完成 | 走 PARA_ROUTING（不算刪）|
| LLM 自動產的 audit report 過 90 天 | 可直接刪（在 wiki/reports/）|
| 使用者明確說「不要任何痕跡」 | git rm 直接刪（極少數）|

---

## 相關

- [[CLAUDE]] §2 規則 C — PARA 五層永不刪除既有檔案
- [[CLAUDE]] §10 規則 E — 寫檔前先提案
- [[Wiki_維護觸發規則]] §4 — Archive / Delete 場景
- [[WIKI_TODO]] — 待清理項目追蹤

← 回到 [[wiki/index]]
