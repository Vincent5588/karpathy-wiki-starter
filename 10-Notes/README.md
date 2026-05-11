# 10-Notes — 永久筆記（atomic + longform 並存）

> **PARA 第 1 層：你「整理好的、想長期保留」的個人筆記**

## 📌 用途（給人）

放**經過你思考、用自己語言寫的永久筆記**。不是收集（那是 00-Inbox 的事），不是專案進度（那是 20-Projects 的事），不是查資料（那是 40-Resources 的事）——是**你的觀點、你的綜合、你的個人作品**。

**兩種類型並存**：

| 類型 | 性質 | 範例 |
|------|------|------|
| **Atomic（Zettelkasten 卡片）** | 一張卡一個概念，會被 LLM ingest 抽 entity | 想到的點子、對某概念的綜合 |
| **Longform（完整作品）** | 一份完整心得 / 敘事 / 長文，**不拆** | 旅遊心得、完整書評、個人觀點長文 |

**典型內容**：
- 讀了 5 篇文章後你綜合出的一個觀點（atomic）
- 想到的點子（已成形、能寫成一段話）（atomic）
- 對某概念的個人理解（不只是抄筆記）（atomic）
- 旅遊心得 / 流水帳（longform）
- 完整書評（你想當「一份作品」保留，不是知識卡片）（longform）

## 🗂 子資料夾建議

```
10-Notes/
├── atomic/          ← Zettelkasten 卡片（會被 LLM 引用做 entity source）
├── longform/        ← 完整心得 / 敘事 / 長文（不拆）
├── journal/         ← 日記式紀錄
└── （或直接平鋪）
```

或不分子資料夾，靠 frontmatter `atomize:` 區分（見下方）。

## 🏷 frontmatter 慣例

```yaml
---
title: "..."
type: longform              # 或 atomic / journal
atomize: false              # longform 必加，atomic 不加（預設 true）
status: draft | stable
created: YYYY-MM-DD
---
```

**`atomize: false`** 告訴 LLM「這份不要拆 atomic」。Obsidian Properties 面板會自動顯示為 checkbox。

## ✅ 何時放東西進來

- 從 `00-Inbox/` 經過你思考後，把**個人觀點版本**寫到這裡
- LLM 路由建議：「這份適合放 10-Notes 嗎？」你同意後放
- 自己直接寫永久筆記（不必經過 inbox）

## 🤖 LLM 行為規範

- ✅ 可從 raw 提案搬到 10-Notes（依 [[CLAUDE]] 規則 C + PARA_ROUTING）
- ✅ ingest 時可把這裡的檔當 source 抽 entity 到 `wiki/entities/`
- ❌ **不刪除、不修改既有檔案內容**（規則 C 鐵則）
- ❌ 不重命名（basename 是穩定識別碼，會斷既有 wiki-link）
- ❌ 不主動「整理」資料夾結構（這是你的私人領地）

## 🆚 跟其他層比較

| 層 | 角色 | 跟 10-Notes 差異 |
|---|------|----------------|
| 00-Inbox | 收集站（未消化）| 還沒思考過 |
| **10-Notes** | **你的觀點** | **已消化、長期保留** |
| 20-Projects | 有截止日的工作 | 不是想法、是任務 |
| 30-Areas | 長期關注的領域 | 30 是「主題」、10 是「想法」 |
| 40-Resources | 別人寫的參考資料 | 40 是「他者」、10 是「自己」 |
| `wiki/entities/` | LLM 編譯的知識卡 | LLM 寫的、整個 vault 共用 |

## 💡 子資料夾建議

不強制，但可依主題開：

```
10-Notes/
├── 想法/
├── 概念綜合/
├── 讀書摘要/
└── ...
```

或直接平鋪也行（< 50 個檔時）。
