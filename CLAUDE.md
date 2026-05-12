# LLM Wiki Starter — LLM Wiki 維護指南

> 本檔給進入此 vault 的 LLM agent（Claude Code / Cowork / Codex / Cursor 等）讀。
> 規範你在維護本 vault 時要遵守的結構、慣例、工作流程。
> 模式來源：[Andrej Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
> Plugin release：**karpathy-wiki-pattern v1.4.3**（含 8 skills）
> Vault patch：**v1.7**（Phase 2 拆檔：Rules D-L + Heuristics 1-3 全移出主檔；規則 D 補技術名詞加繁中說明）

---

## ⚡ 新 Session 熱身（必做）

**第一步**：讀 `wiki/PROGRESS.md`——30 秒掌握 vault 當前健康狀態、Top 5 待辦、上次 session 做了什麼。

**最後一步**：session 結束前更新 `wiki/PROGRESS.md` 的「上次 Session 摘要」（1-3 行 bullet）並視需要調整 Top 5 排序。

> TODO 三層分工：`wiki/PROGRESS.md`（開 session 必讀，top 5）→ `wiki/TODO.md`（完整積壓清單）→ `memory/project_*.md`（跨 session project 上下文 Why/背景）

---

## 0. 版本歷程

> **v1.7**（2026-05-12）。完整版本歷程：`CLAUDE_versions.md`。

---

## 1. Vault 結構（三層 + PARA + Zettelkasten）

```
my-wiki/
├── 00-Inbox/               ← Layer 1：唯一 inbox
│   │                          - 所有新素材的入口
│   │                          - 內容唯讀，但檔案會被 ingest / PARA 路由搬走
│   ├── Daily/              ← 每日個人筆記
│   └── longform/           ← inbox 路徑信號：自動觸發 atomize:false（建 1 個 entity 不拆）
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
│   └── PROGRESS.md         ← 新 session 必讀狀態面板
│
├── 10-Notes/               ← PARA: 永久筆記（Zettelkasten）
├── 20-Projects/            ← PARA: 進行中專案
├── 30-Areas/               ← PARA: 長期領域
├── 40-Resources/           ← PARA: 主題參考資料
│   └── <主題>/             （依 domain 內主題建子目錄分類）
├── 50-Archive/             ← PARA: 已封存
├── Templates/              ← 筆記模板
├── Attachments/            ← 圖片 / PDF 附件
├── Wiki操作文件/            ← wiki 維護文件（健康度監控 / 儀表板 / SOP / 觸發規則等）
├── index.md                ← wiki 主目錄（必須能裝進單一 context window）
└── CLAUDE_versions.md      ← CLAUDE.md 版本歷程 SSOT
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
  - **`index.md`**（⚠️ 每次 ingest 必做：新增條目連結 + 更新 header 計數/日期）
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
0. 先跑規則 K Step 0 預檢（判斷 raw 性質，含 atomize 旗標——見 §3.1.1）
1. 讀取 00-Inbox/{path}/{file}
2. 跟使用者確認 / 討論關鍵重點（除非明確說「不要問直接做」）
3. 建立 entity（兩種模式）：
   - atomize: true（預設）：對每個 atomic 概念分別建一個 entity
     a. 推論 domain（reuse-first，已有的 domain 優先用）
     b. 推論 type（標準 **8 種**詞彙，reuse-first；v1.6 反轉 v1.1：取消 longform type，atomize:false 也用 8 種挑選）
     c. 寫到 wiki/entities/<domain>/<type>/<basename>.md
   - atomize: false：整份 raw 合成 1 個 entity（不拆）
     a. 推論 domain（同上）
     b. **type 同 atomize:true 規則挑選**（v1.6 反轉 v1.1：longform 是呈現方式不是 type；依 entity 該屬類別挑 8 種之一）
     c. 寫到 wiki/entities/<domain>/<type>/<basename>.md（不再寫到 longform/ 子資料夾）
     d. frontmatter 加 `atomize: false` marker（呈現方式標記）+ tag `longform`（選用）
     e. body 含 entity wrapper（摘要 + 核心要點 + 關係 sections + 原文 + 待解）
3.5 raw 含圖則下載 + 本地引用（見規則 I）：兩種模式都做
   a. 識別 raw 內所有 ![alt](url) 外部圖片
   b. 下載到 Attachments/<source-basename>/<NN>-<short-desc>.<ext>
   c. entity 引用改本地
4. 為相關既有概念加 backlink（兩種模式都做）
5. 標記與既有 wiki 的矛盾，提醒使用者
6. 更新 index.md（兩種模式都做——atomize:false entity 也算新 entity）
7. 寫 wiki/daily/YYYY/MM/YYYY-MM-DD.md
8. 依 PARA_ROUTING 提案 raw 目的地
9. 等使用者裁決，才搬 raw 檔
10. 同步更新所有引用該 raw 的 entity（frontmatter source: + 內文引用）
11. 回報使用者：影響了哪些頁、矛盾、後續該調查的主題
```

#### 3.1.1 Atomize 判斷（三層優先序 + Longform body 結構，v1.6 反轉 longform-as-type）

LLM 在 Step 0 預檢時依下列三層優先序決定該 raw 怎麼建 entity：

| 優先序 | 來源 | 規則 |
|-------|------|------|
| 1 | frontmatter `atomize:` 明確指定 | 永遠優先（true / false 都尊重）|
| 2 | 路徑含 `longform/` 子資料夾（如 `00-Inbox/longform/`）| 預設 `atomize: false`（**注意**：`longform/` 僅是 inbox 路徑信號，不對應 entity 目錄）|
| 3 | 預設 | `atomize: true`（拆 atomic）|

**重要**：`atomize: false` **不是「跳過 entity 建立」**，是「**建 1 個 entity 不拆**」。所有 cascade（index / daily log / routing）跟標準 ingest 一樣做。

**v1.6 反轉**：v1.1 把「longform 作為第 9 種 type」是混淆「呈現方式（atomize:false）」跟「概念性質（type）」兩個正交維度的決策錯誤。回到 8 種 type：atomize:false 的 entity 仍照「該 entity 該屬什麼性質（system / pattern / concept / process / role / artifact / rule / person）」挑 type，**不論 atomize 值都用同一套 8 種詞彙**。`atomize: false` 純粹是 frontmatter marker 標記「body 含原文 + entity wrapper」呈現方式，不影響 type 維度。

##### atomize:true vs atomize:false 對照（v1.6 更新）

| 步驟 | atomize: true（預設）| atomize: false（longform 呈現）|
|------|---------------------|---------------------------|
| Step 3 建 entity 數 | N 個（每 atomic 一個）| **1 個**（type 同 atomic 規則挑 8 種之一）|
| Step 3 entity 路徑 | `wiki/entities/<domain>/<type>/` | `wiki/entities/<domain>/<type>/`（同左，不另開 longform/）|
| Step 3 entity body | 精煉版 | 摘要 wrapper + 原文完整保留（或連結到原文）|
| Step 3 frontmatter marker | （無）| `atomize: false`（標記呈現方式）+ tag `longform`（選用）|
| Step 4 backlink | ✅ | ✅ |
| Step 6 更新 index | ✅ | ✅ |
| Step 7 daily log | ✅ | ✅ |
| Step 8 PARA routing raw | ✅ | ✅ |

→ **唯一差別**：atomize:false 只建 1 個 entity，body 保留完整長文 + 加 marker。其他完全一樣，**包括 type 維度照 atomic 8 種規則挑選**。

##### Longform entity body 必備結構（兩種模式）

**模式 X — 外部 longform**（網頁文章 / 訪談逐字稿，raw 另外存在 PARA）：

```markdown
# 標題

> 一句話摘要。

## 核心要點

- 重點 1（LLM 從原文提煉 5-7 條，用自己語言）
- ...

## 與其他概念的關係

### 強連結
- [[既有 entity A]] — 關係

### 推斷連結
- [[既有 entity B]] ?? — 推斷

### 深入閱讀
- **原文（完整版）**：[[40-Resources/<domain>/.../X|原檔]]
- 相關 atomic：[[Y]] / [[Z]]

## 待解 / 矛盾（如有）
- ⚠️ ...
```

**模式 Y — 個人 longform**（自己寫的心得 / 旅遊敘事，沒外部 raw）：

```markdown
（模式 X 全部 section）

## 原文
<個人長文完整內容，不拆解>
```

→ 沒有 wrapper 的 atomize:false entity = 違反規則。lint 該偵測「`atomize: false` 但缺核心要點 / 關係 section」並標 🟡（v1.6 起 marker 從 type=longform 改為 atomize:false）。

##### Longform raw 路由目的地（Step 8，v1.6 更新 entity 路徑）

| 內容性質 | raw 路由到 | entity 在 |
|---------|----------|----------|
| 別人寫的完整文章 | `40-Resources/<domain>/<sub>/` | `wiki/entities/<domain>/<type>/<X>.md`（type 依概念性質挑 8 種之一）|
| 個人完整觀點 / 心得 | 不必另外搬（entity 本身即內容）| 同上 |
| 旅遊 / 日記敘事 | `10-Notes/journal/` 或 `30-Areas/<area>/` | 同上 |

##### 用途配套

- 立即可用模板：`Templates/Longform Note.md`（type 留 placeholder，v1.6 起 LLM 依內容挑 8 種之一）
- 預設 longform 資料夾：`00-Inbox/longform/`（**僅 inbox 路徑信號** → 自動觸發 atomize:false；entity 路徑不對應）

**每次 ingest 必更新的檔案清單（速查）**：

| # | 檔案 | 內容 | 步驟 |
|---|------|------|------|
| ① | `wiki/entities/<domain>/<type>/<X>.md` | 新建 / 更新 entity | step 3 |
| ② | `index.md` | 新增條目連結 + 更新計數/日期 | step 6 |
| ③ | `wiki/daily/YYYY/MM/YYYY-MM-DD.md` | 當日詳細異動 | step 7 |
| ④ | entity frontmatter `source:` | routing 完成後更新路徑 | step 10 |
| ⑤ | `Attachments/<source>/` | 下載 raw 中所有外部圖片到本地 | step 3.5 |

#### 3.1.1.1 Step 0.5：內容性質判定（v1.2 新增）

**核心原則**：§3.1.1 的三層優先序判定的是「**初步預設**」，依 metadata 信號（路徑 / frontmatter）給 atomize 旗標。**但 LLM 必須在 Step 1 開始抽 entity 前再做一次「內容性質判定」**——根據 raw 實際內容判斷預設旗標合不合理，**若不合理主動提案切換並等使用者批准**。

**為什麼**：metadata 信號（譬如「使用者放哪個資料夾」）不一定反映內容本質。常見錯配：

- **預設 atomize:true 但內容極度連貫**：完整訪談 / 單一論點長文 / 敘事流 → 拆 atomic 會破壞論證脈絡，建議改 longform
- **預設 atomize:false 但內容含多 atomic 概念**：使用者隨手丟進 `longform/` 但 raw 實際是技術教學含多獨立可重用概念 → 強行建 1 longform 會浪費 atomic 抽取機會

**內容判定四 criteria**（LLM 讀完 raw 後自問）：

| Criterion | atomic 信號（拆）| longform 信號（不拆）|
|-----------|----------------|--------------------|
| **獨立概念數** | ≥ 3 個可獨立成立的概念（有獨立定義 + 可獨立引用）| ≤ 2 個核心概念，其餘是支撐論證 |
| **論證結構** | 並列式（多個對等小節）| 線性式（單一論點層層展開，拆會斷）|
| **後續引用價值** | 多個概念都會被其他 entity 引用 | 整份作為一個整體被引用 |
| **語境完整性** | 拆出的 atomic 各自完整可懂 | 拆出來脫離脈絡會誤導 |

→ 3-4 個 criterion 偏 atomic = `atomize: true`；3-4 個 criterion 偏 longform = `atomize: false`；2-2 平衡 → 預設旗標保留，但 chat 報告時點出「邊界 case」讓使用者決定。

**LLM 主動提案 SOP**（規則 E show before write 配套）：

1. 讀 raw 內容（至少前 50 行 + 各章節 H2 標題）
2. 跑 4 criterion 判定
3. **若內容判定 ≠ 預設旗標**：在 chat 提案：
   - ❌ 不要直接執行
   - ✅ 寫一段「我看了內容，建議切換成 X 模式，理由：A criterion、B criterion、C criterion。要嗎？」
   - 等使用者回 "yes" / "no" / 修改建議
4. **若內容判定 = 預設旗標**：直接執行，但 chat 報告開頭一句話確認「內容判定 = 預設旗標 X，繼續」

**範例 1：default 路徑但內容該 longform**

```
使用者：ingest 00-Inbox/某城市三天旅遊紀錄.md（atomize 預設 true）

LLM 內容判定：
- 獨立概念數：1（旅遊敘事，無多個獨立 atomic）
- 論證結構：線性敘事
- 引用價值：整份作為一個旅遊紀錄被引用
- 語境完整：拆會破壞時間順序

→ 4/4 偏 longform

LLM 提案：
「raw 看起來是線性敘事的旅遊紀錄，不適合拆 atomic（拆會破壞時間順序 + 語境）。
建議搬到 00-Inbox/longform/ 走 atomize:false 建 1 個 longform entity？
還是你想保持預設 atomize:true 強拆？」

使用者：好，搬 longform
LLM：[執行 mv + 建 longform entity]
```

**範例 2：longform 路徑但內容多 atomic**

```
使用者：ingest 00-Inbox/longform/某工具 8 個進階技巧.md（atomize 預設 false）

LLM 內容判定：
- 獨立概念數：8 個可獨立成立的技巧（每個都可單獨引用）
- 論證結構：並列式（8 個 H2 對等小節）
- 引用價值：每個技巧都可能被其他 entity 引用
- 語境完整：各技巧獨立可懂

→ 4/4 偏 atomic

LLM 提案：
「raw 雖然放 longform/ 子目錄，但內容是 8 個獨立技巧的並列式結構，每個都值得獨立 atomic entity 給其他 entity 引用。
建議覆寫成 atomize:true 抽 8 個 atomic entity？
還是你刻意要保留為 1 個 longform（譬如想保留完整脈絡 + 不希望被引用打散）？」

使用者：你說的對，拆吧
LLM：[建多個 atomic entity 而非 1 個 longform]
```

**例外（不必提案的 case）**：

- frontmatter `atomize:` **明確指定**（譬如使用者已寫 `atomize: true` 或 `false`）→ 永遠 honor，不必再判定
- 使用者**明確要求**「直接走預設」/「不要再問」→ skip 內容判定
- 內容判定結果跟預設旗標**一致**（4/4 或 3/4 偏向預設方向）→ 直接執行，chat 報告開頭一句話確認

**反模式警覺**：

- ❌ 不要每次 ingest 都做冗長的 4 criterion 報告——只在**預設旗標跟內容判定衝突**時才在 chat 提案
- ❌ 不要把內容判定當「使用者選錯資料夾」的指責——這是 LLM 對 raw 內容做的客觀分析，不是糾正使用者
- ❌ 不要假設 longform/ 路徑下的檔一定該 longform——使用者可能隨手丟錯，內容判定是雙保險

### 3.2 Query — 查詢

當使用者問問題（如「根據 wiki，X 跟 Y 的差異是」）：

```
1. 先讀 index.md 找相關概念
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

### type 詞彙說明（v1.6 反轉 longform-as-type，回 8 種）

| type | 意義 | 範例 |
|------|------|------|
| `process` | 流程 / SOP / 工作流 | 每週回顧流程、部署 SOP |
| `concept` | 抽象概念 / 模型 / 原理 / 分析比較 | Zettelkasten、PARA、上下文壓縮、兩工具對比 |
| `role` | 角色 / 職責 | 產品經理、Scrum Master |
| `artifact` | 具體文件 / 報表 / 範本 | 季報模板、需求規格書 |
| `pattern` | 可重複使用的技巧 / 工程模式 | Chain of Thought、5-Why、雙階段架構 |
| `system` | 系統 / 服務 / 工具 / 具體 feature | Obsidian、Notion、GitHub Actions、某產品的某 feature |
| `rule` | 規則 / 政策 / 約束 | 程式碼規範、命名慣例 |
| `person` | 真實人物 | Andrej Karpathy |

**v1.1 暫加的第 9 種 `longform` v1.6 廢除**——longform 是呈現方式（用 `atomize: false` marker）不是概念性質。

**呈現方式 marker（v1.6 起獨立於 type）**：

- `atomize: false` frontmatter：標記「body 保留完整原文 + entity wrapper」呈現方式
- tag `longform`（選用）：給 query / 篩選用

呈現方式 marker 不影響 type 維度——entity 仍按概念性質挑 8 種之一。**body 必含 wrapper**（摘要 + 核心要點 + 關係 section + 原文 + 待解）——詳見 §3.1.1。

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

## 5. index.md 維護規則

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

### 規則 D：英文 quote 必加繁中翻譯（v1.3.6）

> 引用英文 quote 必須緊接繁中翻譯；英文技術名詞必加繁中說明 `Term（中文）`。詳細：`wiki/rules/rule-D-quote-translation.md`。

**Why**：繁中 vault 英文 quote 不翻破壞閱讀流暢度；技術名詞不加對照破壞可搜尋性。**How to apply**：每次 quote 必翻；技術名詞首次出現必加說明；code block / 純標題除外。

### 規則 E：寫檔前先提案（show before write）（v1.3.6）

> 任何寫入動作（新建檔、大改 entity、移動、frontmatter 異動、批次操作）**必須先 show → 使用者確認 → 才動手**。詳細：`wiki/rules/rule-E-show-before-write.md`。

**Why**：AI 寫錯後的修復成本遠高於提案確認成本。**How to apply**：使用者說「直接改」後 ≤30 分鐘內可省略；新建檔 / 改 CLAUDE.md 永遠要提案。

### 經驗法則 1：同源 ingest 整批一起審（v1.3.6）

> 同一份 raw ingest 出 N 個 entity，其中一個升 stable → **其他 N-1 個應一次性整批審查升 stable**。詳細：`wiki/rules/heuristic-1-batch-ingest.md`。

**Why**：同源 entity 可信度一致，沒理由分散處理。**How to apply**：跑 wiki-status-promote 時看到 stable entity → 推薦同 source 的 draft 整批進候選清單。

### 經驗法則 2：同主題第 2 篇 raw → 補 source 而非建新 entity（v1.3.7）

> 新 raw 跟既有 entity ≥ 70% 重疊 → **補 `source:` + bump `updated`，不建新 entity**。詳細：`wiki/rules/heuristic-2-second-source.md`。

**Why**：多 source = 可信度加乘；新建 v2 = wiki-link 分裂 + 違反 reuse-first。**How to apply**：ingest 前先跑 wiki-query；< 70% 重疊或有新 atomic 才建新 entity。

### 規則 H：stable artifact 改動必加版本歷程（v1.3.8）

> `status: stable` 的 artifact 每次有意義改動（≥ 3 行 / 新增章節）必須在檔案內維護 `## 0. 版本歷程` table。詳細：`wiki/rules/rule-H-version-history.md`。

**Why**：`updated:` 只有日期，版本表才能回答「這次改了什麼」。**How to apply**：draft / 短頁免加；artifact / 長 doc / 多次迭代的 stable entity 必加；不確定就加。

### 規則 I：raw 含圖必下載到 Attachments + entity 本地引用（v1.3.11）

> raw 含 `![alt](https://...)` 外部圖片 → **必下載到 `Attachments/<source>/<NN>-<desc>.<ext>` + entity 改用本地引用**。詳細：`wiki/rules/rule-I-image-localization.md`。

**Why**：外部 CDN 連結會壞 + vault 不自包含。**How to apply**：Claude Code session 直接 curl；web-restricted session 產 download script 給使用者執行。

### 規則 J：entity 必繁中 + 翻譯責任前移到產出階段（v1.3.22）

> wiki entity / map / index 全部繁體中文（J.1）；英文專有名詞加中英對照 `Term（中文）`（J.2）；英文 quote 加繁中翻譯（J.3）。詳細：`wiki/rules/rule-J-translation-policy.md`。

**Why**：逐字翻譯成本高；NotebookLM 繁中摘要品質夠 + token 少。**How to apply**：英文 YT / 網頁 → NotebookLM 產繁中報告 → 從報告抽 entity；簡中 → ingest 時順手簡轉繁。

### 規則 K：raw 預檢 SOP（v1.3.22）

> ingest 前 **Step 0 必偵測 raw 性質**並依類型路由（YT URL / 英文文章 / 繁中完整 / Web Clipper clip）。詳細：`wiki/rules/rule-K-raw-precheck.md`。

**Why**：不能假設 raw 已是可 ingest 狀態。**How to apply**：讀 raw 前 100 行 → 對照分流表 → 提案（規則 E）→ 等批准。

### 規則 L：未來新規則 / 經驗法則直接拆檔（v1.3.23）

> 新規則 > 30 行 / 跨多 sub-section / 含長 case study → **直接寫 `wiki/rules/rule-X.md`，主檔只留 1-row 速查 + 連結**。詳細：`wiki/rules/rule-L-self.md`。

**Why**：CLAUDE.md 主檔有上限；progressive disclosure 讓 LLM 開 session 快速掌握，細節 fetch 即可。**How to apply**：規則 A / B / C + Quick Reference 永遠 inline；其餘 > 30 行的全拆出。

### 規則 M：執行心法

> 詳細：`wiki/rules/rule-M-execution-philosophy.md`

**4 條核心執行紀律**：
- **M.1 Reality Checker**：default NEEDS WORK，要 evidence 才說 done
- **M.2 Minimal Change Engineer**：只做被要求的最小 diff，不做額外重構
- **M.3 Code Reviewer**：5 維度（正確性/安全性/效能/可維護性/風格）+ 三級分類（must-fix / should-fix / nit）
- **M.4 Codebase Onboarding**：facts only，不推斷沒看到的東西

**How to apply**：寫檔前自問 M.1+M.2、寫完後 M.3 self-review、寫進 doc 的內容過 M.4。

### 規則 N：雲盤 + git 紀律（single-writer policy）

> 詳細：`wiki/rules/rule-N-cloud-git-discipline.md`

**核心鐵則**：vault 用雲盤跨機同步編輯 OK，但 **git operations 只在一台機器** 的「**雲盤外**」位置進行。多寫者必爆雲盤 conflict（雲盤對 `.git/index` / `refs/heads/main` / objects 製造多版本衝突），單寫者紀律是唯一可靠解。

**三層架構**：

```
[雲盤 vault]（純檔案，跨機 sync）
   ↓ sync 腳本（rsync / robocopy）
[雲盤外 git working tree]（單寫者，~/git-mirrors/ 或 D:\vault-git\ 等）
   ↓ git push / pull
[GitHub]
```

**How to apply**：vault 編輯任何機器 OK（雲盤自動 sync）→ git push 只到「主寫者機」的「雲盤外」git working tree → 其他機器**不該有** `.git/` working tree。多寫者觸發條件（必要 case）：第二人協作 / 主寫者機長期不在 / hardware failure，否則一律單寫者。

**配套**：雲盤無 ignore 機制，per-machine config（workspace.json / settings.local.json 等）仍會撞 → 偶爾跑 cleanup script（範本見拆檔），保留主版刪 `* N.json` 衝突累積。

### 規則 O：Discovery Before Action（探勘優先）

> 詳細：`wiki/rules/rule-O-discovery-before-action.md`

**核心鐵則**：執行任何 ingest / cascade update / 規範改動前**必先**跑 Discovery 三步（ls → 讀必讀檔 → confirm ground truth vs doc drift），不能憑「自以為了解」直接動作。違反就是 drift 來源。

**Why**：LLM 在 vault 工作最深盲點是「不先發現就跳動作」。**規則 E（output 紀律：寫前先 show）+ 規則 M.4（claim 紀律：facts only no inference）+ 規則 O（input 紀律：執行前先探勘）= LLM 行為紀律完整三角**。三條都 codify 才能避免「output / claim / input」三層 drift。**根本原則**：靠規則約束不靠 LLM 自律——LLM 自律下個 session 就忘，規則寫進 CLAUDE.md 永遠在 system prompt。

**How to apply**：

(1) **行為層 Read 工具用法**：default 讀全文（不確定就讀全文 = default safe）；Read 工具預設讀 2000 行，加 limit 是錯誤的自我約束；大檔（>2000 行）先 grep H2/H3 結構再 selective。反模式：對未讀過規範加 `limit:80` / 用 grep 取代 Read。

(2) **文件層 `_` 前綴 = SSOT 慣例**：`_README.md` = 進該資料夾必讀 SSOT、`_MOC.md` = 該主題結構索引 hub、`_skill-staging/` = skill source 編輯區（不是 plugin 載入點）。看見 `_` 前綴 = 立刻讀全文。每次 ingest 必讀基準清單：`CLAUDE.md` + `Wiki_維護觸發規則.md` + 對應 `rule-X.md` + domain `_MOC.md` + 目標 `_README.md`。

(3) **SOP 層 Discovery 三步**：ls 探勘（看見 `_` 立刻讀）→ 讀必讀檔（不加 limit）→ confirm ground truth vs doc drift（不一致時 chat 報告 + 提案修哪邊，規則 E 配套）。

(4) **Reference Discipline（v1.1 新增）**：引用 / 描述既有檔案 / entity / 路徑前**必先 ls / grep verify** canonical name + 實際狀態，不憑印象寫 `[[basename]]` 或「X 未實施」之類描述。常見錯配：wikilink basename 大小寫 / spacing 寫錯造成 dangling link 被 Obsidian auto-create 空檔；模糊詞「應該 / 大概 / 待確認」= 沒 verify 的暗號，verify 後改用「已確認 / 不存在 / mtime 為 Z」明確詞。

---

### 經驗法則 3：「文件即真理」失效要回查 source（v1.3.8）

> 文件寫對但行為錯 ≥ 2 次 → **一定是 doc-vs-code drift**，直接讀 build output / 鎖定版本 source / 實際 config，不再 debug 行為。詳細：`wiki/rules/heuristic-3-doc-rot.md`。

**Why**：文件腐化是必然；quiet failure（exit 0 但實際壞掉）是最隱蔽的 drift 信號。**How to apply**：重要 config 段落加 `# NOTE:` 指向文件章節；定期 diff actual config vs doc。

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

← 回到 [[index|index.md]]
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
