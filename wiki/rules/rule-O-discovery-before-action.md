---
title: "規則 O：Discovery Before Action（探勘優先）"
tags: ["claude-md-rule", "rule-O", "discovery", "ssot", "read-tool", "ls-before-action", "drift-prevention"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-11
updated: 2026-11-17
---

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-11 | 初版——從同 root cause「不先發現就跳動作」連環踩 N 次的 vault 維護經驗 codify。**根本原則**：靠規則約束不靠 LLM 自律——LLM 自律下個 session 就忘，規則寫進 CLAUDE.md 永遠在 system prompt 內 |
| v1.1 | 2026-05-11 | **§O.4 Reference Discipline 新增**：v1.0 codify 後同 root cause 又踩 2 次——(a) 憑印象描述「某檔未實施」沒先 ls；(b) 寫 `[[basename]]` wikilink 沒 grep 確認 canonical basename，dangling link 被 Obsidian auto-create 成空檔。**Pattern 共通**：「reference / 描述既有檔案時憑印象，沒先 ls / grep verify」。**§O.1-O.3 講「進來時讀」，§O.4 補「出去前 verify」**——引用 / 描述既有檔案 / entity / 路徑前必先 ls / grep 確認 canonical name + 實際狀態，不憑印象 |
| v1.2 | 2026-11-17 | **§O.2.5 主題層新增 ＋ §O.3 由三步改四步（Step 0 grep 主題）**：§O.2 的讀取清單全部是路徑導向，掃不到「主題的知識庫不在我要寫的路徑上」這種缺口——這是規則本身的覆蓋盲區，不是執行不確實。同步自 Vincent5588 規則 O v1.2 |
| v1.3 | 2026-11-17 | **取消固定開場與全讀清單**，改為「先判斷任務 → 搜尋候選 → 只讀命中的 SSOT」。選中的規範可完整讀，但不得因不確定而掃完整個 vault；`_MOC`／`_README` 只在任務路由到該層時觸發。同步自 Vincent5588 規則 O v1.3 |

# 規則 O：Discovery Before Action（探勘優先）

> **核心鐵則**：先判斷任務，再搜尋候選並讀取命中的 SSOT；執行 ingest / cascade update / 規範改動前，必跑 Discovery 四步（grep 主題 → ls → 讀命中的 SSOT → confirm ground truth vs doc drift）。不能憑「自以為了解」直接動作，也不能把 Discovery 誤解成每次全讀。

## Why

LLM 在 vault 工作時最深的盲點是「**不先發現就跳動作**」。表現有 3 層：

| 層 | 行為盲點 | 後果 |
|---|---------|------|
| **行為層** | `Read(path, limit:80)` 部分讀大 CLAUDE.md / 不先 `ls` 探勘新資料夾 / 只讀「自以為相關」的檔 | 拿錯規範、放錯位置、漏看 `_README` |
| **文件層** | CLAUDE.md 沒明寫「ingest 前必讀清單」/ `_` 前綴慣例沒 codify / references/ 沒 hub 頁 | LLM 不知該讀什麼，憑印象瞎找 |
| **SOP 層** | 沒「Discovery before Action」結構性反射 / 沒先路由就讀或直接動手 | 上下文被無關內容淹沒，或因漏讀命中的 SSOT 產生 drift |

→ 規則 O 把 3 層全 codify。**根本原則**：靠規則約束，不靠個別 LLM 自律。LLM 自律在下個 session 就會忘；規則寫進 CLAUDE.md 永遠在 system prompt。

## §O.1 行為層 — Read 工具正確用法

LLM 應先縮小到與任務有關的檔，再決定讀取深度。**選中的 SSOT** 若篇幅可控就讀全文，不要自我保守加 limit；但不要把「讀完整個選定檔」擴張成「讀完整個資料夾或 vault」。

### 用法決策表

| 場景 | 該做 | 為什麼 |
|------|------|--------|
| 首次接觸新規範 / 新 hub / 新 entity | **讀全文**（< 500 行直接讀；500-2000 行也直接讀）| 不知道哪段重要，limit 會切到 context |
| 大檔（> 2000 行）| 先 `grep '^## \|^### '` 看 H2/H3 結構 → selective Read 對應段 | Read 工具上限 2000 行 |
| 確認某段（已知 line range）| `Read(offset=N, limit=K)` 精準讀 | 已 know what to read |
| 看 metadata / frontmatter only | `Read(limit:15-20)` | 只要 frontmatter |
| **不確定該讀哪裡** | 先查索引／檔名／關鍵字，找出候選後再讀 | 不確定不是掃完整個 vault 的理由 |

### 反模式

- ❌ 對未讀過的規範檔加 `limit:80`——會切掉重要 context（譬如 §3.1.1.1 在 line 200+ 而你只讀到 80）
- ❌ 「我大概知道」就跳過 Read——LLM「大概知道」≠ vault 規範現況，文件會 drift
- ❌ Read 結果 < limit 就以為讀完了——`limit:200` 但檔有 1000 行只讀了 1/5
- ❌ 用 grep 取代 Read——grep 出 line numbers 後**必須** Read 該段 context，不能只看 grep 摘要

### 例外（可加 limit）

- 大檔已知結構，只要某段 verify（譬如「verify line 150 含 X」）
- 確認 mtime 或 file size 用 `ls -la`，不必 Read
- chat 內已展示過完整內容，回查時 selective 即可

## §O.2 文件層 — 按任務觸發 + `_` 前綴 SSOT 慣例

### `_` 前綴 = SSOT（Single Source of Truth）

vault 內 `_` 開頭檔 / 資料夾**不是隨意命名**，是文化慣例：**該位置的 ground truth**。

| `_` 前綴 | SSOT 語意 | 行為 |
|---------|----------|------|
| `_README.md` | 該資料夾操作與內容 SSOT（譬如 `40-Resources/<topic>/_README.md`）| 任務路由進該資料夾時讀取 |
| `_MOC.md` | 該主題的結構索引 hub（Dataview / Map of Content）| 任務涉及該主題時先讀 |
| `_skill-staging/` | skill source 編輯區（**不是** plugin 載入點）| 知道改這裡是 source-of-truth |
| `_unsorted/` | 未分類 bucket（暫存區）| 處理時 review 內容 |

→ `_` 前綴表示高權威，不表示每次開場都要讀；路由命中時才觸發，命中後不得漏讀。

### 按任務觸發的讀取清單（v1.3）

| 任務觸發 | 讀取檔案 |
|---|---|
| 寫入／移檔／ingest／改規範 | `CLAUDE.md` 相關規則 ＋ [[Wiki_維護觸發規則]] 相關節 |
| 規範版本或歷程 | `Wiki操作文件/CLAUDE_versions.md` |
| 索引／entity 計數 cascade | 根目錄 `index.md` |
| 特定規則操作 | 對應 `wiki/rules/rule-X.md` |
| 特定 domain／project | 對應 `_MOC.md` |
| 進入有操作說明的資料夾 | 對應 `_README.md` 或 README |

未命中就不讀；命中後不得漏讀。

## §O.2.5 主題層 — 路徑導向探勘掃不到的那個缺口（v1.2）

> §O.2 的清單是「路徑導向」的——沿著「我**要寫的檔**在哪」展開：目標資料夾、對應 domain `_MOC`、目標 README。
>
> **它掃不到這一種缺口：「我要寫的主題另有一個知識庫，但它不在我要寫的路徑上。」**

### 必加的一步

寫任何**事實性規格**（schema／欄位／API／外部系統流程／查詢範式）前：

```bash
grep -ril "<主題關鍵字>" 40-Resources/ wiki/entities/   # vault 寫過這個主題嗎
```

並檢查**有無對應 skill**（skill 描述往往直接寫著它涵蓋什麼）。

### 一句話心法

> **先問「vault 寫過這個主題嗎」，再動筆寫。**

### 觸發實例（維護者的 vault）

在某個專案資料夾寫「外部系統的組織資料存取層」規格時，路徑導向清單**全部照做**（CLAUDE.md、觸發規則、專案 `_MOC` 都讀了），卻沒查 `40-Resources/` 裡已經有的**該系統實測 schema 筆記**，也沒用描述第一句就寫著「涵蓋該系統的表與 View 結構」的 skill。**結果自行推導的四項有三項是錯的**——設計了多表 JOIN，其實系統早有現成的安全 View、別的專案正在用；把主管鏈寫成單一欄位，其實是三層 fallback；把「查到多筆」當異常擋掉，其實那是離職再入職的正常情況。

⚠️ 結構性成因：那個知識庫資料夾**原本不在任何一張結構圖上**。

---

## §O.3 SOP 層 — Discovery 四步

任何 ingest / cascade update / 規範改動前**必跑**：

### Step 0：grep 主題（v1.2）

```bash
grep -ril "<主題關鍵字>" 40-Resources/ wiki/entities/
```

見 §O.2.5。**寫事實性規格時這一步不可省。**

### Step 1：ls 探勘

```bash
ls <目標資料夾>/
```

看見什麼：
- `_README.md` / `_MOC.md` → 任務路由命中該層時讀取（SSOT）
- 其他 entity / 檔案 → 看結構分布（資料夾深度、命名 pattern）
- 子目錄 → 必要時 `ls -R` 或 `find <path> -maxdepth 3 -type d`

### Step 2：讀命中的 SSOT

按 §O.2 的任務觸發表讀取；選中的短檔讀全文，長檔（> 2000 行）先 grep H2/H3 結構再讀相關段落。不要把未命中的檔加入固定清單。

### Step 3：Confirm ground truth vs doc drift

```bash
# 看 doc 寫的 vs 實際 ls 看到的
# 譬如 doc 寫「ingest 後 raw 搬 40-Resources/<domain>/某子目錄/」
ls 40-Resources/<domain>/  # 確認該子目錄是否真的存在
```

**不一致時** chat 報告：

```
⚠️ doc drift 觀察：
- doc 寫「raw 搬到 X」
- 實際 ls 看到 X 不存在 / 該位置已改名 Y
- 提案：(a) 更新 doc 跟 ground truth 一致 / (b) 建 X 對應結構

要哪個？
```

→ 規則 E 配套：show before write，這裡 show 的是「doc vs reality 差異」。

## §O.4 Reference Discipline — 引用 / 描述既有檔案前必先 verify（v1.1 新增）

§O.1-O.3 講「**進來時讀**」（執行任務前讀必讀檔）。§O.4 補「**出去前 verify**」：當你要**引用 / 描述 / 報告**既有檔案、entity、路徑、狀態時，**必先 ls / grep verify**，不憑印象。

### 核心鐵則

| 動作 | 必做的 verify |
|------|--------------|
| 寫 `[[basename]]` wiki-link | 先 `find <vault>/wiki/entities -name '*basename*'` 確認 canonical 大小寫 + spacing |
| 寫「X 檔已過時 / X 未實施」 | 先 `ls -la X` 看 mtime + 開檔 verify 實際內容 |
| 報告「vault 內 N 個 entity」 | 先 `find <vault>/wiki/entities -name '*.md' \| wc -l` 算精確值 |
| 描述「Y 資料夾結構長這樣」 | 先 `ls Y/` 或 `find Y -maxdepth 3 -type d` 看實際結構 |
| 引用「規範第 N 條」 | 先 grep / Read 該規範現況，不憑 session 內早期 memory |
| 提案修檔（show before write）時的「現況」描述 | 先 Read 該檔當前內容，不憑 session 早期記憶 |

### 兩個踩雷實例（v1.1 觸發 case）

**Case A：憑印象寫「未跟進」**

```
LLM 寫：「X 已實施 PROGRESS.md / Y vault 未跟進（待確認）」
使用者打臉：「你又漏看，Y vault 有 PROGRESS.md」
ls 確認：PROGRESS.md 確實存在
根因：沒 ls 就憑印象寫「未跟進」
```

→ 該寫的：先 `ls <path>` 後再描述狀態，不憑印象。

**Case B：dangling wikilink 觸發 Obsidian auto-create**

```
LLM update entity 時加：[[name-with-hyphens]]（kebab-case）
真實 entity basename：Name With Spaces（PascalCase + spaces）
→ wiki-link dangling
→ Obsidian auto-create 空檔
→ vault 內多 1 個 0-byte garbage 檔
根因：沒 find / grep 確認 canonical basename 就憑印象寫 wikilink
```

→ 該寫的：先 `find wiki/entities -iname '*keyword*'` 確認 canonical basename。

### SOP（出去前 verify 三步）

```
任何「reference / describe / report 既有檔案」之前必跑：

Step 1：搜尋
  - wikilink target → find <vault>/wiki/entities -name '*<keyword>*'
  - 檔案存在性 → ls -la <path>
  - 內容狀態 → Read 該檔（不加 limit）+ ls -la 看 mtime

Step 2：判斷 canonical
  - 找到多個 candidates？選最近 mtime + status: stable 的
  - 名稱不確定？看 entity frontmatter aliases 列表
  - 完全不存在？標記「待新建」而非「未跟進」

Step 3：寫的時候用 verified canonical 形式
  - wiki-link：用實際檔 basename（注意大小寫 + spacing）
  - 狀態描述：用 verified 事實（譬如「X 5/11 建，含 A / B / C section」）
  - 路徑：絕對路徑（避免相對路徑歧義）
```

### 反模式警覺

- ❌ **「我記得 X 在 Y 位置」就直接寫**——記憶 ≠ 現況，vault 持續演進
- ❌ **「basename 大概是 X」就寫 wikilink**——大小寫 / spacing 不對 = dangling = Obsidian auto-create 空檔
- ❌ **「session 早期 chat 內看過」就不再 verify**——session 內檔狀態可能已被當前任務改動
- ❌ **描述用模糊詞（「應該」「大概」「待確認」）**——這些詞 = 沒 verify 的暗號，verify 後改用「已確認」明確詞

### 例外條款

- 純概念性質的引用（沒指特定檔 / entity）→ 可不必 verify
- 已在當 session 同任務內 verify 過 + 沒中斷 → 可暫時 trust（但跨任務必重 verify）
- 範例 / 教學文字內的 placeholder（譬如 `[[<vault>/X]]`）→ 不是真實引用，不必 verify

### 跟 §O.1-O.3 的關係

| Sub-rule | 紀律方向 | 觸發場景 |
|----------|---------|---------|
| §O.1 行為層（Read 用法）| 選中的檔讀全 | 接到任務、開檔讀 |
| §O.2 文件層（`_` 前綴 SSOT + 按任務觸發）＋ §O.2.5 主題層 | 進來時讀對檔 | 知道哪些檔該讀、這個主題寫過沒 |
| §O.3 SOP 層（Discovery 四步）| 進來時 + confirm doc drift | 動手前 |
| **§O.4 Reference Discipline**（**v1.1 新增**）| **出去前 verify** | 寫 / 引用 / 描述既有 |

→ §O.1-O.3 是 input 紀律的「讀」面；§O.4 是 input 紀律的「verify before reference」面。完整 input discipline 兩面齊。

## 跟其他規則的關係

vault LLM 行為紀律完整三角：

| 規則 | 紀律方向 | 對應 vault 場景 |
|------|---------|----------------|
| **規則 E** | **output 紀律**：寫前先 show | LLM 動寫檔操作前 |
| **規則 M.4** | **claim 紀律**：facts only no inference | LLM 在 doc / chat 講事實時 |
| **規則 O** | **input 紀律**：執行前先探勘（本檔）| LLM 接到任務、動手前 |

3 個互補但 distinct。三條都 codify 才能避免「output / claim / input」三層 drift。

## 反模式警覺

- ❌ **「我記得 vault 規範是 X」就直接動作**——記憶 ≠ 規範現況，vault 持續演進，記憶會 stale
- ❌ **看見 `_README.md` 跳過**——`_` 是 SSOT 信號，不是裝飾
- ❌ **Read 加 limit 「節省 token」**——比起 Read 全文，drift 後補修的 token 更多
- ❌ **因為不確定就掃完整個 vault**——上下文被無關內容淹沒，反而漏看命中的那份
- ❌ **用 grep 摘要當完整 reading**——grep 給 line numbers 是 navigation aid，不是 substitute
- ❌ **doc drift 不報告**——看到 doc vs reality 不一致只「自己消化」不 chat 報告，下次 session 又踩同雷

## 例外條款

- 純 chat 對話（不寫檔 / 不動 vault state）→ 可省 Discovery
- 已在當 session 同個任務內讀過命中的檔 + 沒中斷 → 不必重讀（chat context 還在）
- 緊急修補（譬如 lint score 突降需立刻定位）→ 走「grep → 修 → 補 Discovery」反向流程，事後補讀

## Compounding Engineering 體現

規則 O 本身是 [[Compounding Engineering]] 飛輪的範例：

1. **同 root cause 踩 N 次** → 識別 pattern
2. **Codify 進規則** → 寫進 CLAUDE.md / 拆檔 wiki/rules/rule-X.md
3. **下個 session LLM 預設讀進 system prompt** → 不再憑記憶
4. **規則 H 版本歷程紀錄** → 規則自身的演進可追溯

→ 不靠個別 LLM 自律，靠規則系統演進。
