---
title: "Wiki 維護實戰手冊"
tags: [playbook, cookbook, troubleshooting, vault-meta]
domain: wiki
type: playbook
status: draft
maintained_by: LLM
created: 2026-01-01
updated: 2026-01-01
cssclasses: [wide]
---

# 📖 Wiki 維護實戰手冊

> 收集「常見維護劇本」cookbook。跟 [[CLAUDE]] / [[Wiki_維護觸發規則]] 不同——那兩份講「應該怎做」，本檔講「實際遇到 X 怎辦」。
>
> ⚠️ **空樣板**：累積 1-2 個月實際使用經驗後才有料寫。第一次遇到的「卡住情境」由 LLM 提案加進本檔。

---

## 📚 劇本目錄

> 隨使用累積 case 後填入。預設 placeholder：

- [ ] 1. Lint 跑出 50+ orphan 怎辦？
- [ ] 2. Ingest 撞 basename collision 怎辦？
- [ ] 3. 同個概念被兩個 raw 各 ingest 一份怎合併？
- [ ] 4. Stable entity 發現內容過時怎處理？
- [ ] 5. Plugin 升版後 lint 跑不出來怎 debug？
- [ ] 6. PARA 資料夾結構亂了想重整怎辦？
- [ ] 7. 大量 raw 累積在 00-Inbox/ 該怎麼批次清？

---

## 🎬 劇本範例骨架

> LLM 第一次寫劇本時依此格式：

```markdown
## N. <情境一句話描述>

### 🚨 觸發場景

- 使用者說「...」
- 或系統狀態出現 ...

### 🔍 診斷步驟

1. 跑 `xxx` 看 ...
2. grep `yyy` 確認 ...
3. ...

### 🛠 處理方案

#### 方案 A（推薦）
- 適用：...
- 步驟：1. 2. 3.

#### 方案 B（備案）
- 適用：...
- 步驟：1. 2. 3.

### ❌ 避免做

- 不要 ...
- 不要 ...

### 📝 紀錄到哪

- daily log 加一行
- 健康度若有變動 → [[Wiki_健康度監控]] 追加 row

### 🔗 相關規則

- [[CLAUDE]] §X 規則 Y
```

---

## 💡 跟其他維護檔的分工

| 檔案 | 角色 |
|------|------|
| [[CLAUDE]] | 規範（「應該做什麼」）|
| [[Wiki_維護觸發規則]] | Cascade matrix（「做完該動哪些檔」）|
| **本檔** | **劇本**（「實際遇到 X 怎麼做」）|
| [[Wiki_刪檔處理SOP]] | 單一動作的詳細 SOP |
| [[WIKI_TODO]] | 待辦追蹤 |

---

## 📝 寫劇本的維護紀律

- **何時加新劇本**：第一次遇到該情境 + LLM 跟使用者花 > 10 分鐘解決 → 加進本檔避免下次再卡
- **何時改既有劇本**：第二次遇到、發現原方案不夠好 → bump 內容 + 在 §0 加版本歷程
- **何時砍劇本**：plugin 升版或 vault 結構變動後該情境不再發生 → 移到 50-Archive

---

## 相關

- [[CLAUDE]] — vault 主規範
- [[Wiki_維護觸發規則]] — cascade matrix
- [[Wiki_儀表板]] — 健康狀態快照
- [[WIKI_TODO]] — 待辦追蹤

← 回到 [[wiki/index]]
