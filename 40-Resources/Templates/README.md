# Templates — 筆記模板

> **預製的筆記模板，配合 Obsidian 核心「模板」或 Templater 外掛使用**
> 位置：`40-Resources/Templates/`（v1.13 起從根目錄搬到這裡）。Obsidian 的模板資料夾已預設指向這裡（`.obsidian/templates.json`）；**搬動或改名要同步改那個檔**。

## 📌 用途（給人）

放可重複使用的**筆記骨架**。新建特定類型的筆記時，先套模板再填內容，避免每次重打 frontmatter。

## 📄 內建模板

| 模板 | 用途 | 何時用 |
|------|------|--------|
| `New Entity.md` | wiki entity 骨架（含完整 frontmatter）| 想手動建 entity 時（不走 LLM ingest）|
| `Longform Note.md` | 整篇保留、不拆開的長文 entity 骨架 | 遊記、完整書評這類要保留全文的內容 |
| `Wiki Daily Log.md` | LLM 操作日誌骨架 | LLM 每日首次操作時自動建 `wiki/daily/YYYY/MM/YYYY-MM-DD.md` |
| `Personal Daily.md` | 個人 daily note 骨架 | 你自己寫 `00-Inbox/Daily/YYYY-MM-DD.md` 時 |
| `Mermaid 圖範本.md` | Mermaid 圖的深色樣式碼（共用開頭、九類語意色、完整範例、用 Pele 匯出）| 畫任何 Mermaid 圖時，從這裡複製（規則 W）|

## ✅ 怎麼用

**方法 A — Obsidian 核心「模板」（內建模板用這個）**
1. 模板資料夾已預設為 `40-Resources/Templates`（設定 → 核心外掛程式區的「模板」→ 模板資料夾位置，可確認）
2. 命令面板（`Ctrl/Cmd + P`）→ 輸入「插入模板」→ 選模板
3. 內建模板用的是核心寫法 `{{date}}`、`{{title}}`，插入時會自動換成日期與檔名

**方法 B — Templater 外掛（自己寫進階模板時用）**
1. 設定 → Templater → Template folder location 填 `40-Resources/Templates`（這個設定存在每個人自己的電腦上，模板沒辦法替你帶過去）
2. Templater 的寫法是 `<% tp.date.now() %>` 這種；**它不會替換 `{{date}}`**，所以內建模板請用方法 A
3. 可設「新檔自動套對應模板」（譬如 `wiki/entities/**` 自動套某個 Templater 模板）

**方法 C — LLM 套模板**
跟 Claude 說「依 `40-Resources/Templates/New Entity.md` 建一個關於 X 的 entity」。

**每日筆記**：設定 → 每日筆記 → 模板檔案位置填 `40-Resources/Templates/Personal Daily`（新檔案儲存目錄 `00-Inbox/Daily`，資料夾要先建）。

## 🤖 LLM 行為規範

- ✅ ingest 新 entity 時參考 `New Entity.md` 的 frontmatter 結構
- ✅ 寫 daily log 時依 `Wiki Daily Log.md` 骨架
- ❌ **不修改既有模板**（除非使用者明確要求 + show before write）
- ❌ 不刪模板
- ✅ 可**新增**模板（譬如使用者說「以後 meeting note 都用這格式」→ 建 `40-Resources/Templates/Meeting Note.md`）

## 🔧 自訂 / 擴充

加自己的模板：

```
40-Resources/Templates/
├── New Entity.md           ← 內建
├── Longform Note.md        ← 內建
├── Wiki Daily Log.md       ← 內建
├── Personal Daily.md       ← 內建
├── Mermaid 圖範本.md        ← 內建
├── Meeting Note.md         ← 你新增
├── Book Summary.md         ← 你新增
└── ...
```

**命名建議**：簡單標題（Obsidian 模板選單顯示用）

## 💡 模板 vs entity

| 概念 | 性質 |
|------|------|
| Template | **骨架**（frontmatter + section 標題 + 提示）|
| Entity | **內容**（依骨架填好的實體）|

模板的屬性是空的佔位，不受規則 X 檢查；entity 才有 draft/stable/deprecated 三態。

## 💡 跟 wiki/rules/ 的差異

| 資料夾 | 角色 |
|--------|------|
| **40-Resources/Templates/** | 筆記**骨架**（給 Obsidian 用） |
| **wiki/rules/** | 拆出的**規範詳細文件**（給 LLM 讀，配合 CLAUDE.md 規則 L）|
