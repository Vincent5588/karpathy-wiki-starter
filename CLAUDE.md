# LLM Wiki Starter — LLM Wiki 維護指南

> 本檔給進入此 vault 的 LLM agent（Claude Code / Cowork / Codex / Cursor 等）讀。
> 規範你在維護本 vault 時要遵守的結構、慣例、工作流程。
> 模式來源：[Andrej Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
> Plugin release：**karpathy-wiki-pattern v1.4.3**（含 8 skills）
> Vault patch：**v1.0**（模板初版）

---

## ⚡ 新 Session 熱身（必做）

**第一步**：讀 `wiki/PROGRESS.md`——30 秒掌握 vault 當前健康狀態、Top 5 待辦、上次 session 做了什麼。

**最後一步**：session 結束前更新 `wiki/PROGRESS.md` 的「上次 Session 摘要」（1-3 行 bullet）並視需要調整 Top 5 排序。

> TODO 三層分工：`wiki/PROGRESS.md`（開 session 必讀，top 5）→ `wiki/TODO.md`（完整積壓清單）→ `memory/project_*.md`（跨 session project 上下文 Why/背景）

---

## 0. 版本歷程

> **維護規則**：每次 bump version 時，在此 table 倒序追加新 row（最新在最下方）。

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| **v1.0** | **2026-01-01** | 模板初版建立（基於 karpathy-wiki-pattern v1.4.3，規則 A-M）|

---

## 1. Vault 結構（三層 + PARA + Zettelkasten）

```
my-wiki/
├── 00-Inbox/               ← Layer 1：唯一 inbox
│   │                          - 所有新素材的入口
│   │                          - 內容唯讀，但檔案會被 ingest / PARA 路由搬走
│   └── Daily/              ← 每日個人筆記
│
├── wiki/                   ← Layer 2：LLM 維護的編譯產物
│   ├── entities/           ← v1.3 階層：<domain>/<type>/<basename>.md
│   │   └── <domain>/       （你的主題，如 work / learning / personal）
│   │       ├── concept/    （抽象概念 / 原理）
│   │       ├── process/    （流程 / SOP）
│   │       ├── system/     （系統 / 工具）
│   │       ├── pattern/    （可重複使用的技巧）
│   │       ├── rule/       （規則 / 政策）
│   │       ├── artifact/   （具體文件 / 報表）
│   │       ├── role/       （角色 / 職責）
│   │       └── person/     （真實人物）
│   ├── maps/               ← 跨主題 mermaid 地圖
│   ├── daily/              ← 每日 wiki 操作日誌（按年月分層）
│   ├── rules/              ← 拆出的規則詳細文件
│   ├── index.md            ← 主目錄（必須能裝進單一 context window）
│   └── PROGRESS.md         ← 新 session 必讀狀態面板
│
├── 10-Notes/               ← PARA: 永久筆記（Zettelkasten）
├── 20-Projects/            ← PARA: 進行中專案
├── 30-Areas/               ← PARA: 長期領域
├── 40-Resources/           ← PARA: 主題參考資料
│   └── <主題>/             （依 domain 內主題建子目錄分類）
├── 50-Archive/             ← PARA: 已封存
├── Templates/              ← 筆記模板
└── Attachments/            ← 圖片 / PDF 附件
```

---

## 2. 三大規則（最重要）

### 規則 A：00-Inbox/ 內容唯讀，但檔案會被路由

- ✅ 你**讀** 00-Inbox/ 內檔的內容
- ❌ 你**永不**修改 00-Inbox/ 內檔的內容
- ✅ ingest 完成後，依 PARA_ROUTING 可以**移動** inbox 檔到 PARA 子資料夾（10-Notes / 20-Projects / 30-Areas / 40-Resources / 50-Archive）
- ❌ 你**永不**重新命名 inbox 檔（basename 是穩定識別碼，重新命名會斷既有引用）
- 理由：inbox 內容是真理錨點；但 inbox 根目錄不該長期堆檔

### 規則 B：wiki/ 完全由你維護

- 攝取（Ingest）→ 建/改 `wiki/entities/<domain>/<type>/` 頁面
- **必須同步**：
  - **`wiki/index.md`**（⚠️ 每次 ingest 必做：新增條目連結 + 更新 header 計數/日期）
  - **`wiki/daily/YYYY/MM/YYYY-MM-DD.md`**（每次操作必寫日誌，見 §15）
- 每頁必有 frontmatter（含必填欄位 `domain`、`type`、`status`——詳見 §4）

### 規則 C：使用者 PARA 資料夾（00-50, Templates）= 原始檔保留區

**核心原則**：10-Notes / 20-Projects / 30-Areas / 40-Resources / 50-Archive **五層全部都是原始檔保留區**，LLM **永不刪除、永不修改既有檔案內容**。

- ❌ **永不刪除** 10/20/30/40/50 內任何既有檔案
- ❌ **永不修改** 10/20/30/40/50 內既有檔案內容（除非使用者明確要求）
- ❌ **永不重新命名** 10/20/30/40/50 內既有檔案（basename 是穩定識別碼）
- ✅ **允許寫入**：PARA_ROUTING 把 raw 檔從 00-Inbox 搬到對應 domain 內子分類子資料夾
- ✅ **允許移動到更後段**：把 20-Projects 已完成的搬到 50-Archive（保留歷史，不是刪除）
- ✅ **使用者明確要求** 改 / 刪某檔時才動

**PARA → domain → 子分類 三層結構**：

```
40-Resources/                ← Layer 1: PARA 大類
├── learning/                ← Layer 2: domain 分類
│   ├── 閱讀筆記/            ← Layer 3: 子分類（依主題）
│   └── 課程摘要/
├── work/
│   ├── 會議紀錄/
│   └── 專案文件/
└── ...
```

→ **不要**用 `sources/` 統一塞所有 raw。**要**依 domain 內主題建子目錄分類。

**理由**：
- PARA 是「整理過」的位置——LLM 該尊重既有結構
- 整理動作只能是「往後 archive」（保留歷史），不是「刪掉」
- 要刪 / 大改 PARA 內檔 → 先搬 50-Archive → 30 天後再決定

---

## 3. 四個核心操作

### 3.1 Ingest — 攝取新素材

當使用者說「處理 00-Inbox/xxx」、「ingest xxx」、「依 CLAUDE.md 處理這份檔」：

```
0. 先跑規則 K Step 0 預檢（判斷 raw 性質，決定是否需要前處理）
1. 讀取 00-Inbox/{path}/{file}
2. 跟使用者確認 / 討論關鍵重點（除非明確說「不要問直接做」）
3. 對每個 atomic 概念：
   a. 推論 domain（reuse-first，已有的 domain 優先用）
   b. 推論 type（標準 8 種詞彙，reuse-first）
   c. 寫到 wiki/entities/<domain>/<type>/<basename>.md
3.5 raw 含圖則下載 + 本地引用（見規則 I）：
   a. 識別 raw 內所有 ![alt](url) 外部圖片
   b. 下載到 Attachments/<source-basename>/<NN>-<short-desc>.<ext>
   c. entity 引用改本地
4. 為相關既有概念加 backlink（避免孤兒頁）
5. 標記與既有 wiki 的矛盾，提醒使用者
6. 更新 wiki/index.md（⚠️ 必做：新增條目連結 + 更新 header 計數/日期）
7. 寫 wiki/daily/YYYY/MM/YYYY-MM-DD.md（⚠️ 必做，見 §15）
8. 依 PARA_ROUTING 提案 raw 目的地
9. 等使用者裁決，才搬 raw 檔
10. 同步更新所有引用該 raw 的 entity（frontmatter source: + 內文引用）
11. 回報使用者：影響了哪些頁、矛盾、後續該調查的主題
```

**每次 ingest 必更新的檔案清單（速查）**：

| # | 檔案 | 內容 | 步驟 |
|---|------|------|------|
| ① | `wiki/entities/<domain>/<type>/<X>.md` | 新建 / 更新 entity | step 3 |
| ② | `wiki/index.md` | 新增條目連結 + 更新計數/日期 | step 6 |
| ③ | `wiki/daily/YYYY/MM/YYYY-MM-DD.md` | 當日詳細異動 | step 7 |
| ④ | entity frontmatter `source:` | routing 完成後更新路徑 | step 10 |
| ⑤ | `Attachments/<source>/` | 下載 raw 中所有外部圖片到本地 | step 3.5 |

### 3.2 Query — 查詢

當使用者問問題（如「根據 wiki，X 跟 Y 的差異是」）：

```
1. 先讀 wiki/index.md 找相關概念
2. 讀對應 wiki/entities/<domain>/<type>/X.md（不是讀 raw/）
3. 綜合答案，引用用 [[wiki-link]]（用 basename，Obsidian 自動解析路徑）
4. 如果 wiki 有缺：告訴使用者「wiki 沒這部分，要我從 00-Inbox/{x} ingest 嗎？」
5. 如果這次的分析有持久價值，問使用者：「要不要存成 wiki/entities/<domain>/<type>/Z.md？」
```

### 3.3 Lint — 健康檢查

當使用者說「lint」、「檢查 wiki」、「巡 wiki」：

```
1. 掃 wiki/entities/ 全部頁面（遞迴穿過 <domain>/<type>/）
2. 列出問題：
   - 孤兒頁（沒有 backlink 的 entity）
   - 矛盾聲明
   - 缺失概念（被 [[X]] 引用但沒對應頁）
   - god-nodes（inlinks 多但內文薄）
   - source: 路徑壞掉
3. 對每個問題，提建議。不自動修補，等使用者批准
4. 列出值得新 ingest 的主題
5. 給健康度評分（0-100）
6. 在當日 daily 追加 lint 紀錄
```

> ⚠️ lint 只偵測 + 提建議，**不修補**。批量修補用 wiki-repair skill。

### 3.4 Migration / Backfill — 一次性結構升級

當 plugin 升版或結構規範變動，需要一次性整理既有 entity：

```
1. 觸發詞：「整理現有 entities」、「backfill」、「把舊的也分類」
2. 走 wiki-ingest 的 Mode B：
   a. 掃 wiki/entities/ 全部 .md
   b. 對每份檔推論新的 <domain>/<type>
   c. 產 dry-run plan（移動表 + frontmatter 改動表）
   d. 等使用者批准（"go" / "execute" / "looks good"）
3. 執行：建新資料夾 → 改 frontmatter → 移檔（basename 不變）
4. 跑一次 lint 看健康度有沒有掉
```

---

## 4. wiki/entities/ 頁面格式

### 必要 frontmatter

```yaml
---
title: "頁面標題"
type: process | concept | role | artifact | pattern | system | rule | person
                                  # 標準 8 種詞彙（不能自創）
domain: work | learning | personal | project | <你的主題>
                                  # 主題域，kebab-case ASCII，reuse-first
status: draft | stable | deprecated
tags: [主題1, 主題2]
source:
  - "[[原始檔 basename]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases: [別名1]                  # 選填
---
```

### type 詞彙說明

| type | 意義 | 範例 |
|------|------|------|
| `process` | 流程 / SOP / 工作流 | 每週回顧流程、部署 SOP |
| `concept` | 抽象概念 / 模型 / 原理 | Zettelkasten、PARA、上下文壓縮 |
| `role` | 角色 / 職責 | 產品經理、Scrum Master |
| `artifact` | 具體文件 / 報表 / 範本 | 季報模板、需求規格書 |
| `pattern` | 可重複使用的技巧 / 用法 | Chain of Thought、5-Why 分析法 |
| `system` | 系統 / 服務 / 工具 | Obsidian、Notion、GitHub Actions |
| `rule` | 規則 / 政策 / 約束 | 程式碼規範、命名慣例 |
| `person` | 真實人物 | Andrej Karpathy |

### status 詞彙精確化說明

| 值 | 何時用 | 誰決定 | 對 LLM 的意義 |
|---|------|------|------|
| **`draft`** | 剛 ingest 或內容仍在迭代 | 系統預設 | LLM 引用時應加「（draft，未驗證）」警告 |
| **`stable`** | 經人類審查確認 | **你**（半自動提案 → 你批准） | LLM 可放心引用作為知識依據 |
| **`deprecated`** | 過時 / 被替代 | **你** | LLM 一律**不該**用作答案來源 |

#### 三條鐵則

1. **status 變動永遠需要人類批准**——系統做提案，你做判斷。
2. **stable 是 trust marker，不是 mtime**——stable 代表「我相信這條知識」。
3. **deprecated ≠ delete**——deprecated 是「不要再用、但保留歷史 backlink」。

#### 對 LLM agent 的引用規則

```
status: stable     → 直接引用，不必加註
status: draft      → 引用時必須在句尾加「（draft，未驗證）」
status: deprecated → 不該引用；使用者特別要求才引用，並標明「⚠️ 已 deprecated」
```

### 內容結構建議

```markdown
# 標題

> 一句話定義 / 摘要。

## 為什麼存在 / 核心要點

- 重點 1（用自己語言整合，不直接複製 raw）
- 重點 2

## 與其他概念的關係

### 強連結（原文明確提及）
- [[相關概念 A]] — 關係描述

### 推斷連結（LLM 認為相關，待確認）
- [[相關概念 B]] ?? — 推斷描述

### 深入閱讀
- [[40-Resources/X]]

## 來源出處

- [[原始檔]] §章節

## 待解 / 矛盾（如有）

- ⚠️ 此處與 [[相關概念 C]] 描述衝突，待釐清
```

---

## 5. wiki/index.md 維護規則

- **必須能裝進單一 context window**（建議 < 4000 token）
- 用主題分類組織（按 domain，再依 type 細分），不用平鋪
- 條目格式：`- [[X]] — 一行摘要（< 30 字）`（用 basename）
- 超過 100 條時，考慮分裂成多個 sub-index（如 `index-work.md`、`index-learning.md`）

⚠️ **每次 ingest 必同步更新**。

---

## 6. 命名規範

### entity 檔名（basename）

- 用主題核心關鍵字，盡量短
  - ✅ `Transformer.md`、`PARA 方法論.md`、`Andrej Karpathy.md`
  - ❌ `Transformer 是一種神經網路架構和注意力機制的組合.md`（太長）
- 中英混用 OK
- 不用底線、用空白：`Layer Normalization.md`（Obsidian wiki-link 友好）
- **basename 是穩定識別碼**：移動資料夾時不換 basename（換了會斷 wiki-link）

### 資料夾

- `<domain>` 與 `<type>` 都 **kebab-case ASCII**
  - ✅ `work`、`learning`、`personal`、`side-project`
  - ❌ `Work`、`我的學習`、`SideProject`
- **reuse-first**：已有的 domain 優先用，別發明同義詞
- type 用標準 8 種；新 type 慎開

### 衝突檢查

寫 entity 之前，檢查：
1. 同 basename 是否已存在於別的 `<domain>/<type>/` → 通知使用者
2. 接近的同義詞是否已存在 → 考慮合併或加區分詞

---

## 7. 與既有資料夾的關係

使用者的 `40-Resources/<主題>/` 裡可能已有各種筆記、文件。這些是**穩定文件，不要動**。

但**可以**從這些文件中抽 atomic 概念建到 wiki/entities/：
- 從 `40-Resources/learning/某本書筆記.md` 抽 `wiki/entities/learning/concept/核心概念.md`
- 從 `40-Resources/work/專案文件.md` 抽 `wiki/entities/work/process/專案流程.md`

抽出時，wiki entity 是**精簡 + 跨主題連結**版，原文件保留為深入閱讀資料。

---

## 8. 衝突處理

### 同 basename 跨 domain

如果同 basename 出現在兩個不同的 `<domain>/<type>` 下：
1. **不要兩邊都建**
2. 必通知使用者，提兩個解法：
   - (a) 合併成一頁（選一個 domain）
   - (b) 改 basename 加區分詞（如「公告系統 (work)」「公告系統 (learning)」）

### 內容衝突（同概念不同陳述）

1. **不要直接改既有頁面**
2. 在新頁開頭加 `⚠️ 衝突` 區塊說明
3. 在既有頁面加 `⚠️ 待釐清` 區塊（指到新頁）
4. 通知使用者：「找到衝突 X vs Y，要怎麼處理？」
5. 等使用者裁決才更新

---

## 9. 你能用的工具

本 vault 建議啟用 Dataview 外掛——可在 index / maps / 任意頁放 query。

### 列出某 domain 全部 entity

```dataview
TABLE WITHOUT ID file.link AS "頁面", type AS "Type", status AS "狀態", updated AS "最後更新"
FROM "wiki/entities"
WHERE domain = "learning"
SORT type, file.name
```

### 最近更新 10 個

```dataview
TABLE WITHOUT ID file.link AS "頁面", domain AS "Domain", type AS "Type", updated AS "最後更新"
FROM "wiki/entities"
SORT updated DESC
LIMIT 10
```

### 找 draft 狀態待審 entity

```dataview
LIST
FROM "wiki/entities"
WHERE status = "draft"
```

---

## 10. 使用者風格偏好與核心規則

### 基本偏好

- 語言：繁體中文為主，技術名詞 / API 名稱 / 程式碼可用英文
- 格式：表格、bullet points 都歡迎，但不要過度
- 簡潔：偏好「能讀完」的長度，不要灌水
- 引用：用 wiki-link `[[ ]]`，不要用 markdown link `[text](path.md)`
- 避免：過度道歉、過度誇讚、過度免責聲明
- 行動：要動手做就動手，不要每件事都先問（但新建檔案必先提案，見規則 E）

> ⚠️ **使用者可依個人喜好修改此節**。上方為預設值。

### 規則 D：英文 quote 必加繁中翻譯

引用任何英文原文 quote 時，**必須**在原文 quote 下方緊接著一條繁中翻譯：

```markdown
> "Original English text from the source."
>
> 繁中：「翻譯。」
```

**規則細節**：
1. 兩條 quote 用空白 `>` 分隔
2. 翻譯前綴用「**繁中：**」三字 + 全形冒號
3. 翻譯本身用「**「」**」全形雙引號包起來
4. 短句（< 10 詞）也要翻
5. 專有名詞 / 技術名詞（RAG / token / API 等）不必翻
6. 若原文有**粗體**強調，翻譯也要對應加粗

**不適用情境**：純技術名詞引用、code block 內的英文、標題書名

### 規則 E：寫檔前先提案（show before write）

> **對檔案系統的任何寫入動作必須先在對話中讓使用者看 → 確認 → 才動手。**

**必須先提案的動作**：
- 建立新 entity / map / daily / log（**新檔**）
- 大規模改 entity 內容（重寫一個 entity 主體）
- 移動 / 改名檔案
- 改 frontmatter 結構（type、domain、status 等）
- 批次操作（wiki-repair 一次改 N 個檔）
- 寫 plugin / skill / 工具腳本

**不需要先提案的動作**：
- 純讀取（Read / Glob / Grep）
- bash 查詢類（ls / find / wc -l）
- 跑 wiki-lint / wiki-query 等唯讀 skill

**提案格式**：
```
我要做：[動作描述]
影響檔案：[路徑列表]
變動內容（節錄）：...

確認後執行？
```

**例外條款**：
- 使用者明確說「直接改」「不要再問」→ 後續 ≤30 分鐘內可省略提案
- 使用者批准了多步驟計畫 → 步驟內的每個動作不必再個別提案
- 但**新建檔案 / 改 CLAUDE.md** 永遠要提案

### 規則 H：stable artifact 改動必加版本歷程

任何 `status: stable` 的 artifact，每次有意義改動（≥3 行內容變動或新增章節）必須在檔案內維護 `## 0. 版本歷程` table：

```markdown
## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | YYYY-MM-DD | 初版建立 |
| v1.1 | YYYY-MM-DD | 主要變動描述 |
```

**例外**：draft / 短頁（< 50 行）不必加。

### 規則 I：raw 含圖必下載到 Attachments + entity 本地引用

當 raw 檔含外部圖片（`![alt](https://...)`）時，**必須下載到本地 + entity 改用本地引用**：

1. 下載到 `Attachments/<source-basename>/<NN>-<short-desc>.<ext>`
2. entity 引用改：`![alt](Attachments/<source>/<NN>-<file>.jpg)`

**例外**：純裝飾圖、版權敏感的圖可省略

### 規則 J：entity 必繁中 + 翻譯責任前移到產出階段

**核心原則**：vault 內全部 wiki entity / map / index 都用**繁體中文**。但翻譯責任前移到 raw 產出階段，不在 ingest 階段做逐字翻譯。

**三條子規則**：

**J.1 — entity 必須全文繁中**：
- entity 標題、frontmatter title、章節標題、列點、表格——全部繁中
- 例外：純命令（bash）、程式碼片段、約定俗成不譯廠商名

**J.2 — 英文專有名詞中英對照**（首次出現時）：
- ✅ `Retrieval-Augmented Generation（檢索增強生成，RAG）`
- ❌ 純英文不譯 / ❌ 純中譯不附原文

**J.3 — 英文 quote 加繁中翻譯**（強化規則 D）

**Raw 各語言的處置**：

| Raw 語言 | 處置 |
|---------|------|
| **繁體中文** | 直接 ingest 抽 entity |
| **英文（YT 影片）** | 走 youtube-to-notebooklm skill → NotebookLM 產繁中摘要報告 → 從報告抽 entity |
| **英文（網頁文章）** | 丟 NotebookLM 產繁中摘要，或直接 50-Archive |
| **簡體中文** | ingest 時順手簡轉繁 + 詞彙台灣化 |

### 規則 K：raw 預檢 SOP

**核心原則**：wiki-ingest 步驟 0 必須先偵測 raw 性質，依類型路由到對應前處理，不要假設 raw「已經是可 ingest 狀態」。

**Step 0 預檢分流表**：

| Raw 內容 | 偵測規則 | 自動提案 |
|---------|---------|---------|
| **frontmatter `pending_action: youtube-skill`** | YouTube 影片 clip | 直接 chain youtube-to-notebooklm |
| **裸 YT URL**（檔長 < 300 bytes + YT URL） | URL-only 偵測 | 「先跑 youtube-to-notebooklm skill 產繁中報告？」|
| **大量英文文章**（≥ 30% 英文 + 檔長 > 5 KB） | 語言比例 | 「丟 NotebookLM 產繁中摘要 → 從摘要 ingest？或直接 50-Archive？」|
| **簡中文章**（含「数据 / 软件 / 这个」等） | 字元偵測 | 「ingest 時順手簡轉繁 + 詞彙台灣化」|
| **繁中 + 結構完整** | 預設 | **直接 ingest**（標準流程）|
| **空檔 / 只有 frontmatter**（body < 50 bytes） | 檔長偵測 | 「raw 內容不足，無法 ingest。要刪嗎？」|

**LLM 收到 ingest 指令時的決策樹**：
```
使用者：「ingest 00-Inbox/X.md」
  ↓
LLM 讀檔前 100 行（step 0 預檢）
  ↓
提案處理路線（規則 E）
  ↓
使用者批准：
  ├─ 「OK」→ 走標準 wiki-ingest 流程
  ├─ 「先跑 X skill」→ chain 對應 skill → 等產出後再 ingest
  └─ 「Archive」→ 移到 50-Archive，不 ingest
```

### 規則 L：未來新規則直接拆檔

**核心原則**：CLAUDE.md 主檔有上限。新規則符合以下任一條件 → 直接寫 `wiki/rules/rule-X.md`，主檔只留 1 row 速查：

- 內容超過 30 行
- 跨多個 sub-section
- 含長 case study
- 預期會持續擴充

**拆檔的 frontmatter 規格**：
```yaml
---
title: "規則 X：xxx"
tags: ["claude-md-rule"]
domain: wiki
type: rule
status: stable
parent: "[[CLAUDE]] §10"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 規則 M：執行心法

> 詳細：`wiki/rules/rule-M-execution-philosophy.md`

**4 條核心執行紀律**：
- **M.1 Reality Checker**：default NEEDS WORK，要 evidence 才說 done
- **M.2 Minimal Change Engineer**：只做被要求的最小 diff，不做額外重構
- **M.3 Code Reviewer**：5 維度（正確性/安全性/效能/可維護性/風格）+ 三級分類（must-fix / should-fix / nit）
- **M.4 Codebase Onboarding**：facts only，不推斷沒看到的東西

**How to apply**：寫檔前自問 M.1+M.2、寫完後 M.3 self-review、寫進 doc 的內容過 M.4。

---

### 經驗法則 1：同源 ingest 整批一起審

當一份 raw 文件 ingest 出 N 個 entity，其中**一個 entity 升 stable**，**其他 N-1 個應一次性審查整批升 stable**——它們的可信度根源於同一個業務確認過的 source。

### 經驗法則 2：同主題第 2 篇 raw → 補 source 而非建新 entity

當不同 raw 描述**同一個主題、同一個概念**，且既有 entity 已存在時：

✅ **正確**：把新 raw 路徑加進既有 entity 的 `source:` 列表，bump `updated`
❌ **錯誤**：建一個「概念 v2」之類的新 entity（重複 = 違反 reuse-first）

---

## 11. Quick Reference

| 使用者說 | 你應該 |
|---------|-------|
| 「處理 00-Inbox/xxx」/「ingest xxx」 | 先跑規則 K Step 0 預檢 → 依分流結果 chain skill 或標準 ingest（§3.1）|
| 裸貼 YT URL（無提示語）| 主動問「要做 YT 報告嗎」→ 跑 youtube-to-notebooklm skill |
| 「整理現有 entities」/「backfill」 | Mode B Backfill（§3.4）|
| 「根據 wiki，問題 Y」 | Query（§3.2）|
| 「巡一下 wiki」/「健康檢查」 | Lint（§3.3）|
| 「批量修 wiki」/「wiki repair」 | wiki-repair skill（先 lint，再 repair --plan-only，使用者批准才動）|
| 「批次升 stable」/「審草稿」 | wiki-status-promote skill |
| 「我加了一份新檔到 00-Inbox/」 | 等具體指示 ingest，**不要自動 ingest** |
| 「整理一下這份」 | 問清楚是要 ingest 到 wiki/ 還是只是摘要 |

---

## 12. 詳細參考

- 完整 LLM Wiki 模式說明：[Andrej Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Plugin skills 文件：`karpathy-wiki-pattern/skills/` 下各 SKILL.md

---

## 13. 工具 SOP — 永遠 recursive 掃 entities/

**鐵則**：任何掃 `wiki/entities/` 的工具必須遞迴。

```python
# ✅ 對
Path("wiki/entities").rglob("*.md")

# ❌ 錯：flat glob 會漏掉子資料夾的檔
Path("wiki/entities").glob("*.md")
```

**Lint 掃描範圍 = inlinks 計算範圍**：lint.py 只掃 `wiki/entities/` + `wiki/maps/`。修復孤兒頁要在這兩個目錄內加 backlink。

---

## 14. Daily Log — 每日異動日誌

所有 ingest / lint / repair / migration 紀錄一律寫到當日 daily（`wiki/daily/YYYY/MM/YYYY-MM-DD.md`）。

### 結構

```
wiki/
├── daily/
│   └── YYYY/
│       └── MM/
│           └── YYYY-MM-DD.md
```

**建檔規則**：寫當日 daily 前，先確認 `wiki/daily/YYYY/MM/` 資料夾存在，不存在則建立。

### 格式

```markdown
---
title: "Wiki Daily Log — YYYY-MM-DD"
tags: ["wiki-daily", "log"]
date: YYYY-MM-DD
cssclasses: [wide]
---

# 📅 YYYY-MM-DD Wiki 異動日誌

## 摘要

| 操作 | 影響頁面 | 備註 |
|------|---------|------|
| ingest | [[某 entity]] | 從 00-Inbox/某檔.md 抽出 |

---

## 詳細

### [操作名稱]

...詳細說明...

---

← 回到 [[index|wiki/index.md]]
```

### `cssclasses: [wide]` 適用檔類

| 類型 | 加 wide？ |
|------|----------|
| daily 異動日誌 | ✅ 預設加 |
| MOC / 監控報表 / 對照表 | ✅ 加 |
| Lint / Repair audit report | ✅ 加 |
| 個別 entity（多半 prose） | ❌ 不加 |
| 個人 daily（00-Inbox/Daily/） | ❌ 預設不加 |

### 觸發時機

- 每次有 Ingest / Repair / Backfill / 大型 Update 操作後
- 單次小修（加 1 條 backlink、改 frontmatter）可以只寫摘要表

---

## 15. Mermaid 渲染規則

**黃金法則**：node label 含特殊字元時一律加引號 `["..."]`。

| 坑 | 觸發 pattern | 正解 |
|----|------------|------|
| Ordered list 解析 | `[1. text]` | 改用圈圈數字 `["① text"]` |
| Parallelogram shape | `[/text]` | 加引號 `["/text"]` |
| HTML tag 誤判 | `[<text]` | 加引號 `["<text>"]` |

寫完必做：在 Obsidian 預覽渲染一次再 commit。

---

## 16. Vault 維護輔助檔清單

> Vault 根目錄預置一組「維護輔助檔」（樣板，內容預設空）。當使用者觸發對應動作時，**LLM 必須主動建立 / 更新對應檔**，不要假設使用者會自己填。

### 16.1 檔案清單與觸發條件

| 檔案 | 內容狀態 | 何時 LLM 該主動更新 |
|------|---------|------------------|
| [[WIKI_TODO]] | 空樣板 | 衍生新待辦 / 完成既有待辦 / 重排優先順序時 |
| [[Wiki_儀表板]] | 空樣板 | 使用者說「巡 wiki」/「初始化儀表板」/「看看狀態」時，依骨架填當前數據 |
| [[Wiki_健康度監控]] | 空樣板 | 每次 `lint` 跑完追加一 row（依規則：[[Wiki_維護觸發規則]] §2）|
| [[Wiki_刪檔處理SOP]] | 空樣板 | 使用者第一次說「刪掉 X」/「不要這個了」時，依骨架走流程 + 填追蹤表 |
| [[Wiki_維護實戰手冊]] | 空樣板 | 使用者跟 LLM 花 > 10 分鐘解決一個維護情境 → 把該情境寫成劇本加進來 |
| [[Wiki_專有名詞對照表]] | 有內容（8 節 ~100 詞）| ingest 新 entity 含未收錄英文專有名詞時 → 加新 row |
| [[Wiki_維護觸發規則]] | 有內容（cascade matrix）| 加新 skill / 改 cascade 邏輯時更新 |
| [[Wiki_Web_Clipper_範本]] | 有內容（3 個 JSON 範本）| 新增範本類型時 bump 版本 + 加 §5.X |

### 16.2 LLM 紀律

- **空樣板 ≠ 不重要**：空樣板是「等真實 case 觸發才填」的設計，**不准刪、不准視為缺檔**
- **第一次觸發**：依檔內骨架填，**不要重新設計 schema**
- **觸發後忘記更新 = 漏 cascade**：[[Wiki_維護觸發規則]] 已列每個動作對應該更新的維護檔
- **使用者主動問「儀表板現在數字是？」**：LLM 即時讀 vault 計算 + 更新 [[Wiki_儀表板]]，不要回「我不知道」

### 16.3 跟 PROGRESS.md / WIKI_TODO 的分工

| 檔案 | 角色 | 何時讀 |
|------|------|-------|
| `wiki/PROGRESS.md` | 新 session 30 秒熱身（最頂層）| 每次新 session 必讀 |
| [[Wiki_儀表板]] | Vault 全景快照（中層）| 想看數字 / 趨勢時 |
| [[WIKI_TODO]] | 完整待辦清單（執行層）| 想排今天做什麼時 |
| [[Wiki_健康度監控]] | Lint 趨勢專屬 | lint 跑完 / 想看健康度走向時 |
| [[Wiki_維護實戰手冊]] | 卡關時翻劇本 | 遇到陌生情境 / 重複情境時 |
