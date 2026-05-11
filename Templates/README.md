# Templates — 筆記模板

> **預製的筆記模板，配合 Templater / 內建模板外掛使用**

## 📌 用途（給人）

放可重複使用的**筆記骨架**。新建特定類型的筆記時，先套模板再填內容，避免每次重打 frontmatter。

## 📄 內建模板

| 模板 | 用途 | 何時用 |
|------|------|--------|
| `New Entity.md` | wiki entity 骨架（含完整 frontmatter）| 想手動建 entity 時（不走 LLM ingest）|
| `Wiki Daily Log.md` | LLM 操作日誌骨架 | LLM 每日首次操作時自動建 `wiki/daily/YYYY/MM/YYYY-MM-DD.md` |
| `Personal Daily.md` | 個人 daily note 骨架 | 你自己寫 `00-Inbox/Daily/YYYY-MM-DD.md` 時 |

## ✅ 怎麼用

**方法 A — Obsidian 內建模板**
1. Settings → Core plugins → 啟用 Templates
2. Settings → Templates → Template folder location 設為 `Templates`
3. Cmd/Ctrl + P → Insert template → 選模板

**方法 B — Templater 外掛（推薦）**
1. 裝 Templater plugin
2. Settings → Templater → Template folder location 設為 `Templates`
3. 可設「新檔自動套對應模板」（譬如 `wiki/entities/**` 自動套 `New Entity.md`）

**方法 C — LLM 套模板**
跟 Claude 說「依 `Templates/New Entity.md` 建一個關於 X 的 entity」。

## 🤖 LLM 行為規範

- ✅ ingest 新 entity 時參考 `New Entity.md` 的 frontmatter 結構
- ✅ 寫 daily log 時依 `Wiki Daily Log.md` 骨架
- ❌ **不修改既有模板**（除非使用者明確要求 + show before write）
- ❌ 不刪模板
- ✅ 可**新增**模板（譬如使用者說「以後 meeting note 都用這格式」→ 建 `Templates/Meeting Note.md`）

## 🔧 自訂 / 擴充

加自己的模板：

```
Templates/
├── New Entity.md           ← 內建
├── Wiki Daily Log.md       ← 內建
├── Personal Daily.md       ← 內建
├── Meeting Note.md         ← 你新增
├── Book Summary.md         ← 你新增
└── ...
```

**命名建議**：簡單英文標題（Obsidian 模板選單顯示用）

## 💡 模板 vs entity

| 概念 | 性質 |
|------|------|
| Template | **骨架**（frontmatter + section 標題 + 提示）|
| Entity | **內容**（依骨架填好的實體）|

模板**永遠 status: stable**（骨架本身穩定），entity 才有 draft/stable/deprecated 三態。

## 💡 跟 wiki/rules/ 的差異

| 資料夾 | 角色 |
|--------|------|
| **Templates/** | 筆記**骨架**（給 Obsidian 用） |
| **wiki/rules/** | 拆出的**規範詳細文件**（給 LLM 讀，配合 CLAUDE.md 規則 L）|
