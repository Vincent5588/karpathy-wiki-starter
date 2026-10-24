# PROMOTE_TEMPLATE — 提案訊息標準格式

> 給 wiki-status-promote skill 用。每筆候選的呈現格式 + 批次摘要範本。

## 單筆呈現格式

### 🟢 建議升 stable

```
[#1] [[折扣上限]]                          🟢 建議升 stable
   orders/rule · created 95 天前 · inlinks=2 · 字數 487 · 上次更新 2026-04-26
   📝 限制最高折扣條件：當訂單有特定 PromoFlag 時，折扣不可超過某上限。
   🔗 backlinks: [[訂單審核流程]], [[折扣審核流程]]
   ✅ 理由：rule 類強制門檻達標 + 內容完整 + 90 天穩定 + 無警示

   動作？[ENTER 升 stable] / [s skip] / [k keep draft] / [d deprecate]
```

### 🟡 建議留 draft

```
[#7] [[微信雲開發]]                          🟡 建議留 draft
   travel/system · created 14 天前 · inlinks=1 · 字數 312
   📝 微信雲開發是騰訊提供的 Serverless 平台...
   🔗 backlinks: [[旅遊規劃的挑戰]]
   ⚠️ 理由：inlinks 少 + 創建未滿 30 天 + 內容偏短
   建議動作：補 2 條 backlink（從 [[小程序開發 lib 選型]] / [[雲開發小程序交付流程]]）後再升

   動作？[ENTER 留 draft + review_by 30天後] / [k keep] / [s skip] / [u upgrade anyway]
```

### 🔴 建議改 deprecated

```
[#15] [[Vibe Coding]]                        🔴 建議改 deprecated
   wiki/concept · created 6 天前 · inlinks=0 · 字數 80
   📝 Karpathy 2025/02 提出的概念，描述...
   🔗 backlinks: 無
   ⚠️ 理由：內容過薄（< 200 字）+ 沒任何 backlink + Growth Signal placeholder

   ⚠️ **覆蓋規則**：此 entity 在 [[wiki/maps/Wiki 索引]] 標記為 "Growth signals（待 ingest）"，
        刻意保留以提示未來 ingest，不該 deprecate。建議改：留 draft + review_by 90 天後。

   動作？[ENTER 改採建議：留 draft] / [d deprecate anyway] / [s skip]
```

## 按 domain 分組總覽

```
📊 wiki-status-promote 候選清單（Mode: Triage）

🏢 orders（共 N 個 draft）
   🟢 建議升 stable（M 個）
      [#1] 折扣上限
      [#2] 運費規則
      ...
   🟡 留 draft（K 個）
      [#3] ...
   🔴 deprecated（J 個）
      [#4] ...

🤖 Claude（共 N 個 draft）
   🟢 ...

[繼續其他 domain]

═══════════════════════════════════════════
總計：A 升 stable / B 留 draft / C deprecated
═══════════════════════════════════════════

👉 動作選項：
  [g go]      逐筆審（從 #1 開始）
  [a all-go]  批准所有 🟢 + 所有 🟡 留 draft + 所有 🔴 改建議（最快）
  [orders]    只跑 orders domain
  [s stop]    放棄
```

## 批次完成後的報告格式

```
═══════════════════════════════════════════
✅ wiki-status-promote 完成（Mode: Triage）

📊 統計
  - 升 stable：35 個
  - 留 draft（含 review_by 提醒）：18 個
  - 改 deprecated：12 個
  - 跳過：0 個

📁 影響檔案
  - 65 個 wiki/entities/*.md（frontmatter 改動）
  - wiki/log.md（+1 行）
  - wiki/daily/2026/05/2026-05-02.md（補一段 §wiki-status-promote）

🎯 vault 狀態變化
  - draft 比例：37% → 10% 🟢
  - stable 比例：63% → 86%
  - deprecated 比例：0% → 7%

═══════════════════════════════════════════
🌀 Compounding 飛輪 — 過程中觀察到的規律？

(列 3-5 個可能的規律供使用者選)
1. 業務規則類即使 inlinks 少也該升 stable
2. 旅遊規劃的工具選型類因為都還在 v1 規劃，留 draft 一段時間是合理的
3. wiki/ growth signals 不該 deprecate（要保留）
...

把覺得對的勾起來，我會寫進 vault CLAUDE.md。也可以說「沒觀察到」跳過。
═══════════════════════════════════════════
```
