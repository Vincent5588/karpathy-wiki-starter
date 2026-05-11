# LLM Wiki Starter

> 一個以 **PARA + Zettelkasten + LLM** 三層架構打造的個人知識庫模板。
> 基於 [Andrej Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

---

## 這是什麼？

這個模板讓你用 AI（Claude）幫你管理個人知識庫。你只需要做一件事：**把想記的東西丟進 `00-Inbox/`，然後告訴 Claude 「幫我整理這個」**。

Claude 會自動：
- 讀懂內容
- 抽出關鍵概念建成知識卡片（entity）
- 幫你把檔案歸到正確的資料夾
- 建立概念之間的連結

---

## 核心概念（10分鐘讀懂就夠用）

### 📁 PARA — 四個桶子

不需要背哲學，只需要記四個問題：

| 資料夾 | 問題 | 範例 |
|--------|------|------|
| `00-Inbox/` | 這個東西我還沒決定放哪 | 剛截圖的文章、剛想到的點子 |
| `20-Projects/` | 這個有截止日、做完就結束 | 準備一個演講、學完一門課 |
| `30-Areas/` | 這個我要長期關注，沒有終點 | 健康、工作技能、理財 |
| `40-Resources/` | 這個以後查資料用 | 某個主題的文章集合、工具說明 |
| `50-Archive/` | 這個不活躍但不捨得刪 | 做完的專案、過時的資料 |
| `10-Notes/` | 這是我整理好的永久筆記 | Zettelkasten 式的個人想法卡片 |

**實際使用**：你 90% 的時間只需要用 `00-Inbox/`，其他的讓 Claude 幫你路由。

---

### 🗃️ Zettelkasten — 連結比儲存更重要

Zettelkasten（德文「卡片盒」）的精神只有一條：

> **一個概念一張卡片，卡片之間互相連結。**

傳統筆記的問題：你記了但找不到，或記了但沒用到。  
Zettelkasten 的解法：每張卡片都連到相關卡片，查一個就能發現全部相關的。

在這個系統裡，每個 `wiki/entities/` 裡的檔案就是一張「知識卡片」（entity）。Claude 會幫你建卡片、建連結。

---

### 🤖 LLM Wiki Pattern — AI 幫你編譯知識

傳統 Zettelkasten 需要你手工抽概念、手工建連結，很累。  
LLM Wiki Pattern 的核心想法：

> **原始素材（raw）在 Inbox，精煉知識（entity）在 wiki/entities/。LLM 做編譯的工作。**

你的角色：收集 + 判斷  
Claude 的角色：閱讀 + 抽概念 + 建連結 + 整理

---

## 5 分鐘 Setup

### 前置需求

- [Obsidian](https://obsidian.md/)（免費）
- [Claude Code](https://claude.ai/code)（需要 Anthropic API key）

### 步驟

**1. Clone 這個 repo**
```bash
git clone https://github.com/<owner>/karpathy-wiki-starter.git my-wiki
```

**2. 用 Obsidian 打開**
- 開啟 Obsidian → Open folder as vault → 選 `my-wiki` 資料夾

**3. 啟用必要外掛**

在 Obsidian Settings → Community plugins → 搜尋並安裝：
- **Dataview**（查詢用）
- **Templater**（模板用，選用）

本 repo 附帶的 `karpathy-wiki-pattern` plugin 需手動複製到你的 vault 外掛目錄，或等待 Obsidian 社群外掛上架。

**4. 啟用 wide-pages CSS snippet（讓表格顯示正常）**

Settings → Appearance → CSS snippets → 啟用 `wide-pages`

**5. 在 vault 根目錄開啟 Claude Code**
```bash
cd my-wiki
claude
```

**6. 測試第一次 ingest**
- 把任何一篇文章複製到 `00-Inbox/test.md`
- 在 Claude Code 說：`ingest 00-Inbox/test.md`
- 看 Claude 怎麼處理

---

## 日常使用流程

### 收集（你做）
把任何東西丟進 `00-Inbox/`：
- 文章截圖 / Web Clipper 抓的網頁
- 會議筆記
- 讀書摘要
- 靈感、想法

### 整理（Claude 做）
```
你：ingest 00-Inbox/某個檔案.md
Claude：讀檔 → 提案 entity → 等你確認 → 建 wiki/entities/ → 搬檔案
```

### 查詢（一起做）
```
你：根據 wiki，解釋一下 XX 跟 YY 的差別
Claude：讀 wiki/entities/ → 綜合回答 → 引用來源
```

### 維護（Claude 做）
```
你：巡一下 wiki（或說：lint）
Claude：掃描所有 entity → 找問題 → 提報告 → 等你決定
```

---

## 資料夾結構說明

```
my-wiki/
├── 00-Inbox/           ← 所有新素材的入口，不要手動整理
│   └── Daily/          ← 每日個人筆記
├── 10-Notes/           ← 整理好的永久筆記（Zettelkasten 風格）
├── 20-Projects/        ← 進行中的專案
├── 30-Areas/           ← 長期關注的領域
├── 40-Resources/       ← 主題參考資料
├── 50-Archive/         ← 封存
├── wiki/               ← AI 維護的知識編譯層（不要手動大改）
│   ├── entities/       ← 知識卡片（domain/type/名稱.md）
│   ├── maps/           ← 跨主題視覺地圖
│   ├── daily/          ← AI 操作日誌
│   ├── index.md        ← 知識主目錄
│   └── PROGRESS.md     ← 新 session 必讀狀態面板
├── Templates/          ← 筆記模板
├── Attachments/        ← 圖片 / 附件
└── CLAUDE.md           ← AI 行為規範（核心）
```

---

## 常見問題

**Q：我不用每個資料夾都嗎？**  
不用。從 `00-Inbox/` 開始就好，其他的 Claude 會幫你路由。

**Q：我的筆記要怎麼命名？**  
放進 `00-Inbox/` 的檔案隨便命名都行。Claude 在整理時會幫你規範。

**Q：wiki/entities/ 裡的檔案我可以手動改嗎？**  
可以，但不建議大改結構。內容補充沒問題，frontmatter 欄位盡量不要手動亂動。

**Q：我需要學 Markdown 嗎？**  
基本的就夠：`#` 標題、`-` 列點、`**粗體**`。其他讓 Claude 處理。

**Q：CLAUDE.md 我需要讀懂嗎？**  
不需要。那是給 AI 看的說明書，你只需要知道「它存在 + 不要刪它」。

---

## 進階：自訂你的 domain

當你積累一定筆記後，你的知識庫會自然形成幾個主題（domain）。  
在 `wiki/entities/` 裡，每個 domain 是一個子資料夾：

```
wiki/entities/
├── work/        ← 工作相關知識
├── learning/    ← 學習筆記
├── personal/    ← 個人成長
└── project-X/  ← 特定專案知識
```

怎麼決定 domain？告訴 Claude：「我想把這些筆記歸到 work domain」，它會幫你。

---

## 授權 & 致謝

- 架構來源：[Andrej Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Plugin：karpathy-wiki-pattern
- 模板維護：歡迎 PR / Issue
