# 40-Resources — 主題參考資料

> **PARA 第 4 層：以後查資料時會用到、不限定特定專案的主題集**

## 📌 用途（給人）

放**他人寫的參考資料**——文章、教學、技術文件、工具說明——以**主題（domain）**組織。跟 10-Notes 不同：這裡放的是別人的內容，不是你的個人觀點。

**典型內容**：
- 某主題的優質文章集
- 工具的使用說明 / cheatsheet
- 訂閱通訊收藏
- 課程講義 / YouTube 摘要
- API / 框架文件節錄

## ✅ 何時放東西進來

每個主題開一個 domain 子資料夾：

```
40-Resources/
├── Claude/
│   ├── 學習指南/
│   └── YouTube 摘要/
├── PKM/
│   ├── Zettelkasten/
│   └── PARA/
├── PM/
│   ├── 框架/
│   └── 案例研究/
└── tools/
    ├── git/
    └── docker/
```

**domain 命名**：kebab-case 英文或繁中皆可，但**同主題只能一個 domain**（不要 `PKM/` 跟 `知識管理/` 並存）。

## 🤖 LLM 行為規範

- ✅ LLM 可從 `00-Inbox/` 把參考資料 raw 路由到對應 `40-Resources/<domain>/<子分類>/`
- ✅ ingest 時把這裡的檔當 source 抽精煉 entity 到 `wiki/entities/`（依使用者明確指定）
- ✅ 路由時依「**reuse-first**」原則——已存在的 domain 優先用，不發明同義詞
- ❌ **不刪除、不修改既有檔案內容**（規則 C）
- ❌ **不要建 `sources/` 統一塞 raw**——要依 domain 內主題建子目錄
- ❌ 不重命名既有檔案
- ❌ **不主動掃描** 40-Resources/ 找東西 ingest（規則 C；使用者明確指定才掃）

## 📥 Longform 路由（atomize: false）

從 `00-Inbox/longform/` 路由過來的 raw（譬如「完整書評」「課程心得長文」「某主題綜合長文」）可以放對應 domain 子資料夾：

```
40-Resources/
├── Claude/
│   ├── 01-基礎/                ← 一般參考
│   └── 完整書評/               ← longform 子分類
│       └── 某本書評.md
├── PKM/
│   └── 心得長文/
│       └── 我對 Zettelkasten 的完整看法.md
```

→ LLM 看 `atomize: false` 時不抽 atomic entity，只搬檔到此 + 寫 daily log。詳見 [[CLAUDE]] §3.1.1。

→ **判斷**：書評 / 心得屬「主題集」性質 → 40-Resources；屬「個人觀點」性質 → 10-Notes/longform/。模糊時問使用者。

## 🆚 跟其他層比較

| 層 | 跟 40-Resources 差異 |
|---|---------------------|
| 10-Notes | 你的觀點 vs **40 是別人的內容** |
| 20-Projects | 跟特定專案綁 vs **40 不綁專案** |
| 30-Areas | 你持續投入的領域 vs **40 是收集的參考** |
| `wiki/entities/` | LLM 編譯的精煉版 vs **40 是原始參考** |

**判斷準則**：「這份資料是我寫的還是別人寫的？」→ 別人寫的 → 40-Resources；「以後其他專案也會查嗎？」→ 是 → 40。

## 💡 三層分類示意

```
40-Resources/                ← Layer 1: PARA 大類
├── Claude/                  ← Layer 2: domain（主題）
│   ├── 01-基礎/             ← Layer 3: 子分類
│   ├── 02-進階用法/
│   └── YouTube 摘要/
├── PKM/                     ← 另一個 domain
│   ├── Zettelkasten/
│   └── BASB/
```

子目錄命名可依使用者偏好：
- 編號式：`01-X / 02-Y / 03-Z`（適合有順序的主題）
- 主題式：`學習指南 / 工具 / 案例`（適合分類）

## 💡 跟 wiki/entities/ 的關係

40-Resources 是 LLM ingest 的主要 source 區。流程：

```
40-Resources/Claude/某教學.md     ← 原始參考（保留）
     ↓ ingest
wiki/entities/claude/concept/X.md  ← LLM 抽出的精煉知識卡（跨主題連結）
```

兩份**並存**——原始參考供深入閱讀，wiki entity 供快速綜合。
