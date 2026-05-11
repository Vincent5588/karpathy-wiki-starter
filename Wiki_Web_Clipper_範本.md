---
title: "Wiki Web Clipper 範本（操作 SOP + JSON）"
tags: ["web-clipper", "obsidian", "setup-guide", "vault-meta", "ingest-pipeline"]
domain: wiki
type: setup-guide
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10 規則 K（raw 預檢 SOP）"
created: 2026-01-01
updated: 2026-01-01
cssclasses: [wide]
---

# 📋 Wiki Web Clipper 範本（操作 SOP + JSON）

> Obsidian Web Clipper 範本設定指南。包含 3 個正式範本（Default / YouTube / GitHub）的完整 JSON、安裝步驟、驗證測試、維護紀律。
>
> **設計目標**：clip 進來的 raw 自帶 frontmatter 預檢線索（`pending_action`），讓 LLM ingest 時依 [[CLAUDE]] §10 規則 K 自動分流到對應 skill（如 youtube-to-notebooklm）。

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-01-01 | 模板初版：Default + YouTube + GitHub 三範本，frontmatter 含 `pending_action` 預檢線索 |

---

## 1. 為什麼存在

每天使用 Obsidian Web Clipper 從各種網頁 / YouTube 影片抓 raw 進 vault，常見問題：

| 問題 | 解法 |
|---|---|
| 預設範本只放 `tags: clippings` 一個字串，後續 LLM 看不到「這是英文 / 中文 / YT / 一般文章」線索 | 範本加 `language` / `word_count` / `type` / `pending_action` 等 frontmatter 欄位 |
| 不同類型 raw（YT / 文章 / GitHub）需要走不同處理流程，但所有 raw 用同一範本就分不出來 | 多範本策略 + URL 觸發器自動分流 |
| 檔名 trailing `.` 造成 `proof..md` 雙點問題 | `safe_name` filter |
| YT 頁面抓 `{{content}}` 會吃進 70 KB transcript，本來該交給 NotebookLM 處理 | YouTube 範本不抓 `{{content}}`，只抓 metadata |
| 中文 article 跟英文 article 走不同路徑（規則 J / K），但 Default 範本沒辦法判斷語言 | frontmatter 加 `language`，LLM ingest 時自動分流 |

**核心信念**：raw 入庫時把預檢能做的事情做完，LLM 後續處理輕鬆 + 一致。

---

## 2. 維護紀律

**何時更新本檔 + 範本 JSON**：

- 觀察某類 raw 進來頻率高 → 開新範本（譬如 arXiv 論文 / Twitter 串 / Reddit 討論）
- Web Clipper 升版改 schemaVersion → 同步本檔 JSON
- 範本實測踩到雷 → bump v1.X，加進 §0 版本歷程

**Cascade 觸發**（依 [[Wiki_維護觸發規則]]）：
- 範本 v 改動 → 同步本檔 §0 + JSON 區塊 + 操作 SOP
- 影響規則 K 預檢邏輯 → 同步 [[CLAUDE]] §10 規則 K

**LLM 自我紀律**：使用者反饋「我新 clip 了個 X 進來」時 → 看 frontmatter `pending_action` 知道下一步 → 依規則 K Step 0 分流。

---

## 3. 安裝步驟

### 3.1 裝 Obsidian Web Clipper 擴充功能

- Chrome / Edge / Brave：[Chrome Web Store](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf)
- Firefox：[Firefox Add-ons](https://addons.mozilla.org/firefox/addon/web-clipper-obsidian/)
- Safari：[Mac App Store](https://apps.apple.com/app/obsidian-web-clipper/id6720708363)

### 3.2 連結 vault

擴充功能首次開啟 → 「設定 → 一般」→ 選你的 vault（路徑通常是 `~/Documents/your-vault-name` 或 iCloud 同步路徑）。

> ⚠️ 每台機器 vault 路徑不同，請依實際 vault 位置選取。

### 3.3 匯入三個範本

1. 設定 → **範本** → 「**新範本**」 → 「**匯入**」
2. 貼下方 [§5 範本 JSON](#5-範本-json) 內容（一個一個來，3 份分開匯入）
3. 完成後左側列表**順序**應該是（從上到下）：

```
✅ 對：
1. YouTube     ← 最上（先 match）
2. GitHub      ← 中（次 match）
3. Default     ← 最下（fallback）

❌ 錯：
1. Default     ← 排最上會吃掉所有 URL
2. YouTube
3. GitHub      ← 永遠匹配不到
```

→ 用左邊 `⋮⋮` 拖把手調整順序，Default 必須**最後**。

### 3.4 驗證測試

clip 幾個 URL 確認分流：

| URL 類型 | 期望範本 | 期望 frontmatter |
|---|---|---|
| `https://www.youtube.com/watch?v=...` | YouTube | `type: youtube-clipping`、`pending_action: youtube-skill` |
| `https://github.com/owner/repo`（repo 首頁）| GitHub | `type: github-clip`、`pending_action: github-skill` |
| `https://github.com/owner/repo/blob/.../file.md`（GitHub 子頁）| Default | `type: web-clipping`、`pending_action: rule-K-precheck` |
| 一般網頁（非 YT / 非 GitHub repo 首頁）| Default | `type: web-clipping`、`pending_action: rule-K-precheck` |

**測試結果應寫到** 當天 wiki daily log（`wiki/daily/YYYY/MM/YYYY-MM-DD.md`）。

---

## 4. 範本順序與觸發器邏輯

Web Clipper 由上到下逐一檢查 `triggers` regex，**第一個匹配的範本就用它**。所以：

```
配置（當前）：
  YouTube   triggers: [yt regex]        ← 先檢查，YT URL 進這邊
  GitHub    triggers: [github regex]    ← 次檢查，GitHub repo 首頁進這邊
  Default   triggers: []                ← fallback，其他 URL 進這邊

未來擴充：
  YouTube   triggers: [yt regex]
  GitHub    triggers: [github regex]
  arXiv     triggers: [arxiv regex]
  ...
  Default   triggers: []                ← 一定要在最後
```

**規則**：
- 有 triggers 的範本要排在**空 triggers（Default）的上面**
- 同類觸發器只能擇一
- Default 範本 triggers 永遠空，當 fallback

---

## 5. 範本 JSON

### 5.1 Default 範本

**用途**：fallback，所有非特殊類別的網頁 raw。

**觸發器**：`（空）`

```json
{
  "schemaVersion": "0.1.0",
  "name": "Default",
  "behavior": "create",
  "noteNameFormat": "{{title}}",
  "path": "00-Inbox",
  "noteContentFormat": "{{content}}",
  "context": "",
  "properties": [
    {
      "name": "title",
      "value": "{{title}}",
      "type": "text"
    },
    {
      "name": "source",
      "value": "{{url}}",
      "type": "text"
    },
    {
      "name": "author",
      "value": "{{author|split:\", \"|wikilink|join}}",
      "type": "multitext"
    },
    {
      "name": "published",
      "value": "{{published}}",
      "type": "date"
    },
    {
      "name": "clipped_at",
      "value": "{{date}}",
      "type": "datetime"
    },
    {
      "name": "description",
      "value": "{{description}}",
      "type": "text"
    },
    {
      "name": "language",
      "value": "{{schema:inLanguage}}",
      "type": "text"
    },
    {
      "name": "word_count",
      "value": "{{content|wordcount}}",
      "type": "number"
    },
    {
      "name": "type",
      "value": "web-clipping",
      "type": "text"
    },
    {
      "name": "status",
      "value": "draft",
      "type": "text"
    },
    {
      "name": "pending_action",
      "value": "rule-K-precheck",
      "type": "text"
    },
    {
      "name": "tags",
      "value": "clippings, raw, pending-precheck",
      "type": "multitext"
    }
  ],
  "triggers": []
}
```

### 5.2 YouTube 範本

**用途**：自動分流給 youtube-to-notebooklm skill 處理。

**觸發器**：`https?://(www\.)?(youtube\.com/watch|youtu\.be/)`

```json
{
  "schemaVersion": "0.1.0",
  "name": "YouTube",
  "behavior": "create",
  "noteNameFormat": "{{title|safe_name}}",
  "path": "00-Inbox",
  "noteContentFormat": "# {{title}}\n\n📺 **YouTube**：{{url}}\n🎙 **頻道**：{{schema:@VideoObject.author.name}}\n⏱ **時長**：{{schema:@VideoObject.duration}}\n📅 **發布**：{{published}}\n\n## 影片描述\n\n{{description}}\n\n---\n\n> 🤖 **待處理（pending-precheck）**：本檔 `pending_action: youtube-skill` → LLM ingest 時自動 chain youtube-to-notebooklm skill 產繁中報告再 ingest entity。\n>\n> 詳見 [[CLAUDE]] §10 規則 K（raw 預檢 SOP）。\n",
  "context": "",
  "properties": [
    {
      "name": "title",
      "value": "{{title}}",
      "type": "text"
    },
    {
      "name": "source",
      "value": "{{url}}",
      "type": "text"
    },
    {
      "name": "youtube_url",
      "value": "{{url}}",
      "type": "text"
    },
    {
      "name": "channel",
      "value": "{{schema:@VideoObject.author.name}}",
      "type": "text"
    },
    {
      "name": "duration",
      "value": "{{schema:@VideoObject.duration}}",
      "type": "text"
    },
    {
      "name": "published",
      "value": "{{published}}",
      "type": "date"
    },
    {
      "name": "clipped_at",
      "value": "{{date}}",
      "type": "datetime"
    },
    {
      "name": "description",
      "value": "{{description}}",
      "type": "text"
    },
    {
      "name": "type",
      "value": "youtube-clipping",
      "type": "text"
    },
    {
      "name": "status",
      "value": "draft",
      "type": "text"
    },
    {
      "name": "pending_action",
      "value": "youtube-skill",
      "type": "text"
    },
    {
      "name": "tags",
      "value": "youtube, raw, pending-precheck, clippings",
      "type": "multitext"
    }
  ],
  "triggers": [
    "https?://(www\\.)?(youtube\\.com/watch|youtu\\.be/)"
  ]
}
```

### 5.3 GitHub 範本

**用途**：clip GitHub repo 首頁時自動分流給 GitHub-to-wiki 流程處理（`gh api` 抓真實 metadata + 寫入 `40-Resources/GitHub/`）。

**觸發器**：`^https?://github\.com/[^/]+/[^/]+/?(\?.*)?$`

- ✅ `https://github.com/anthropics/skills`
- ✅ `https://github.com/anthropics/skills/`
- ✅ `https://github.com/anthropics/skills?tab=readme`
- ❌ `https://github.com/anthropics/skills/blob/main/README.md`（子頁走 Default）
- ❌ `https://github.com/issues`（站內導覽走 Default）

→ **只 clip repo 首頁**才觸發。子頁面（commit / PR / issues）走 Default 範本當一般文章處理。

```json
{
  "schemaVersion": "0.1.0",
  "name": "GitHub",
  "behavior": "create",
  "noteNameFormat": "{{title|safe_name}}",
  "path": "00-Inbox",
  "noteContentFormat": "# {{title}}\n\n🐙 **GitHub URL**：{{url}}\n📝 **Description**：{{description}}\n\n---\n\n> 🤖 **待處理（pending-precheck）**：本檔 `pending_action: github-skill` → LLM ingest 時跑 GitHub-to-wiki 流程（gh api 抓真實 metadata + WebFetch README + 寫入 `40-Resources/GitHub/<owner>-<repo>.md`）。\n>\n> 詳見 [[CLAUDE]] §10 規則 K（raw 預檢 SOP）。\n\n## README clip\n\n{{content}}\n",
  "context": "",
  "properties": [
    {
      "name": "title",
      "value": "{{title}}",
      "type": "text"
    },
    {
      "name": "source",
      "value": "{{url}}",
      "type": "text"
    },
    {
      "name": "github_url",
      "value": "{{url}}",
      "type": "text"
    },
    {
      "name": "description",
      "value": "{{description}}",
      "type": "text"
    },
    {
      "name": "clipped_at",
      "value": "{{date}}",
      "type": "datetime"
    },
    {
      "name": "word_count",
      "value": "{{content|wordcount}}",
      "type": "number"
    },
    {
      "name": "type",
      "value": "github-clip",
      "type": "text"
    },
    {
      "name": "status",
      "value": "draft",
      "type": "text"
    },
    {
      "name": "pending_action",
      "value": "github-skill",
      "type": "text"
    },
    {
      "name": "tags",
      "value": "github-clip, raw, pending-precheck, clippings",
      "type": "multitext"
    }
  ],
  "triggers": [
    "^https?://github\\.com/[^/]+/[^/]+/?(\\?.*)?$"
  ]
}
```

**為何不抽 `github_owner` / `github_repo` frontmatter 欄位**：Web Clipper filter 鏈不確定支援 URL slice 抽取。**改成 LLM ingest 時從 `github_url` 用 `gh api repos/<owner>/<repo>` 同時抽 owner/repo + 拿真實 metadata**——更可靠且一致。

---

## 6. 範本欄位說明

### 6.1 Schema 結構

| 欄位 | 用途 | 必填 |
|---|---|---|
| `schemaVersion` | Web Clipper 範本格式版本，目前 `0.1.0` | ✅ |
| `name` | 範本名稱（左側列表顯示）| ✅ |
| `behavior` | `create`（建新筆記）/ `append` / `prepend` / `overwrite` | ✅ |
| `noteNameFormat` | 檔名模板（含 filters）| ✅ |
| `path` | vault 相對路徑寫入位置 | ✅ |
| `noteContentFormat` | 筆記 body markdown 模板 | ✅ |
| `context` | 額外上下文（通常空字串）| - |
| `properties[]` | frontmatter 屬性陣列 | ✅ |
| `triggers[]` | URL regex 陣列，match 哪個就用此範本 | ✅（Default 為空 array）|

### 6.2 properties 欄位 type

| Type | 用途 | 範例 |
|---|---|---|
| `text` | 單行文字 | `title`、`source`、`channel` |
| `multitext` | 多行 / 陣列 | `tags`、`author` |
| `date` | 日期（YYYY-MM-DD）| `published` |
| `datetime` | 日期 + 時間 | `clipped_at` |
| `number` | 數字 | `word_count` |

### 6.3 模板變數

**內建變數**（Web Clipper 自動抓）：

| 變數 | 抓什麼 |
|---|---|
| `{{title}}` | 頁面 `<title>` 或 `og:title` |
| `{{url}}` | 當前頁面 URL |
| `{{author}}` | meta tag `author` 或 schema.org `author` |
| `{{published}}` | meta tag `article:published_time` 或 schema.org `datePublished` |
| `{{date}}` | 當下時間（clipping 動作時間）|
| `{{description}}` | meta tag `description` 或 `og:description` |
| `{{content}}` | 頁面主要內容（用 [Defuddle](https://github.com/kepano/defuddle) 抽純文）|

**Schema.org 變數**（從頁面 `<script type="application/ld+json">` 抓）：

| 變數 | 抓什麼 |
|---|---|
| `{{schema:inLanguage}}` | 語言（譬如 `zh-TW` / `en`）|
| `{{schema:@VideoObject.author.name}}` | YT 頻道名 |
| `{{schema:@VideoObject.duration}}` | YT 時長（ISO 8601 duration 格式）|

**Filters（pipe 後處理）**：

| Filter | 用途 | 範例 |
|---|---|---|
| `safe_name` | sanitize 檔名（去 `:`、`/`、trailing `.` 等）| `{{title\|safe_name}}` |
| `replace:"X":"Y"` | 字串替換 | `{{title\|replace:":":""}}` |
| `split:"X"` | 切分 | `{{author\|split:", "}}` |
| `join` | 合併 array | `{{...\|join}}` |
| `wikilink` | 包成 `[[ ]]` | `{{author\|wikilink}}` |
| `trim` | 去頭尾空白 | `{{...\|trim}}` |
| `wordcount` | 數字數 | `{{content\|wordcount}}` |

---

## 7. 已知問題 + 回退方案

| # | 問題 | 影響 | 回退方案 |
|---|------|------|---------|
| 1 | YT 頁面 `{{schema:@VideoObject.author.name}}` 抓不到 | `channel` / `duration` 欄空 | 不影響後續 youtube-to-notebooklm，NotebookLM 會自己抓 metadata |
| 2 | Default 範本 `{{content\|wordcount}}` 跑出異常值 | `word_count` 欄位異常 | LLM ingest 時自己 `wc -w` 算，可忽略 |
| 3 | 中文網頁 `{{schema:inLanguage}}` 抓不到 | `language` 欄空 | LLM ingest 時自己偵測，可忽略 |
| 4 | `{{title\|safe_name}}` filter 不認識 | 檔名變 literal 字串 | 改回 `{{title}}` + 規則 K Step 0 改名 |

→ 全部都不影響核心工作流，frontmatter `pending_action` + `type` 是關鍵分流線索，這兩個一定能抓到。

---

## 8. 跟 vault 規則的整合

```
Web Clipper 範本（本檔）
    ↓ 寫入 frontmatter
00-Inbox/<title>.md（含 pending_action / type / tags 預檢線索）
    ↓ LLM 讀檔
[[CLAUDE]] §10 規則 K Step 0 預檢
    ↓ 依 pending_action 分流
    ├─ youtube-skill        → chain youtube-to-notebooklm → NotebookLM 繁中報告
    ├─ github-skill         → gh api 抓 metadata + 寫入 40-Resources/GitHub/
    ├─ rule-K-precheck      → 看 language / word_count 決定下一步
    │                         ├─ 中文 + 結構完整 → 標準 wiki-ingest
    │                         ├─ 大量英文       → 提案丟 NotebookLM 摘要
    │                         └─ 簡中           → 簡轉繁 + 詞彙台灣化 → ingest
    └─ （未來）paper-summarize / 等
        ↓
wiki-ingest 抽 entity
    ↓
[[CLAUDE]] §10 規則 J（entity 必繁中 + 中英對照）
    ↓
wiki/entities/<domain>/<type>/<X>.md
```

**規則對照**：

- [[CLAUDE]] §10 規則 J — entity 必繁中、中英對照、quote 翻譯（**ingest 後**規範）
- [[CLAUDE]] §10 規則 K — raw 預檢 SOP（**ingest 前**分流）
- [[CLAUDE]] §10 規則 D — 英文 quote 加繁中翻譯
- [[CLAUDE]] §10 規則 I — raw 含圖必下載到 Attachments
- 本檔 — Web Clipper 端的 raw 入庫範本設計

---

## 9. 未來範本擴充

當某類 raw 來源頻率高、而 Default 處理不夠用時，加新範本：

### 9.1 候選範本

| 範本 | 觸發 | 用途 | frontmatter 重點 |
|---|---|---|---|
| **arXiv 論文** | `https?://arxiv\.org/(abs\|pdf)/.+` | 論文丟 NotebookLM | `type: paper` / `pending_action: paper-summarize` / `arxiv_id: <ID>` |
| **Twitter / X 推文** | `https?://(twitter\|x)\.com/.+/status/.+` | 短文 / 推串 | `type: tweet` / `pending_action: rule-K-precheck` |
| **Substack / Medium 文章** | `https?://(.+\.substack\.com\|medium\.com/.+)` | 長文閱讀 | `type: longform-article` / `pending_action: rule-K-precheck` |
| **Hacker News 討論** | `https?://news\.ycombinator\.com/item\?id=` | 討論串 + 原文 | `type: hn-discussion` |
| **Reddit 討論** | `https?://(www\|old)\.reddit\.com/r/.+/comments/` | 討論串 | `type: reddit-thread` |

### 9.2 加新範本 SOP

1. **觀察 1-2 週**該類 raw 進來頻率，確認值得開新範本（< 5 個 / 月可能不必）
2. **設計 frontmatter**：哪些欄位有助於 LLM 後續處理？對應 `pending_action` 是什麼？
3. **寫 JSON**：copy YouTube 範本當底，改觸發器 / properties / content 模板
4. **加進本檔 §5**：新增 `### 5.X` section，含完整 JSON
5. **加進本檔 §0 版本歷程**：bump v1.X
6. **更新本檔 §4 範本順序**
7. **匯入到 Web Clipper**，調整左側順序（新範本在 Default 上面）
8. **clip 一個測試 URL 驗證**
9. **Cascade**：[[CLAUDE]] §10 規則 K Step 0 預檢分流表加新 row + [[Wiki_維護觸發規則]] 更新

---

## 10. FAQ

### Q1：為什麼不用 Default 範本一個就好？

A：因為不同類型 raw 需要不同處理：
- YT 影片 → 不該抓 `{{content}}`（70 KB transcript 浪費），應該交給 NotebookLM
- 一般 article → 抓 `{{content}}` 是對的
- 同個範本沒辦法兩種行為，所以分。

### Q2：`safe_name` filter 真的存在嗎？

A：依 Obsidian Web Clipper [filter 文件](https://github.com/obsidianmd/obsidian-clipper/blob/main/docs/filters.md)支援。升級 Web Clipper 後重測確認。

### Q3：YT 範本不抓 content，那要用時間戳目錄怎麼辦？

A：YT 影片的「章節時間軸」通常在 description 內（影片描述底下的 `0:00 章節 1` 那種）。本範本抓 `{{description}}` 已包含這部分。完整 transcript 由 NotebookLM 自己抓字幕，不需要 Web Clipper 抓。

### Q4：clip 進來後想立刻跑 ingest 怎麼喊？

A：跟 LLM 說「ingest 00-Inbox/X.md」或「跑規則 K Step 0」，LLM 會看 `pending_action` 自動分流。

### Q5：新範本（arXiv 等）什麼時候加？

A：§9.2——觀察 1-2 週頻率，超過 5 個 / 月才值得開。先用 Default 範本撐一陣子。

---

## 11. 相關

- [[CLAUDE]] §10 規則 K — raw 預檢 SOP（本範本的下游處理規範）
- [[CLAUDE]] §10 規則 J — entity 必繁中（再下游）
- [[Wiki_維護觸發規則]] — 動作 cascade 表
- [[Wiki_專有名詞對照表]] — 中英對照表
- [[wiki/index]] — vault 主目錄

← 回到 [[wiki/index]]
