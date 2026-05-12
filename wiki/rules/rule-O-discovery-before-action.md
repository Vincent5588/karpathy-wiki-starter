---
title: "規則 O：Discovery Before Action（探勘優先）"
tags: ["claude-md-rule", "rule-O", "discovery", "ssot", "read-tool", "ls-before-action", "drift-prevention"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-11
updated: 2026-05-11
---

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-11 | 初版——從同 root cause「不先發現就跳動作」連環踩 N 次的 vault 維護經驗 codify。**根本原則**：靠規則約束不靠 LLM 自律——LLM 自律下個 session 就忘，規則寫進 CLAUDE.md 永遠在 system prompt 內 |
| v1.1 | 2026-05-11 | **§O.4 Reference Discipline 新增**：v1.0 codify 後同 root cause 又踩 2 次——(a) 憑印象描述「某檔未實施」沒先 ls；(b) 寫 `[[basename]]` wikilink 沒 grep 確認 canonical basename，dangling link 被 Obsidian auto-create 成空檔。**Pattern 共通**：「reference / 描述既有檔案時憑印象，沒先 ls / grep verify」。**§O.1-O.3 講「進來時讀」，§O.4 補「出去前 verify」**——引用 / 描述既有檔案 / entity / 路徑前必先 ls / grep 確認 canonical name + 實際狀態，不憑印象 |

# 規則 O：Discovery Before Action（探勘優先）

> **核心鐵則**：執行任何 ingest / cascade update / 規範改動前，**必先**跑 Discovery 三步（ls → 讀必讀檔 → confirm ground truth vs doc drift），不能憑「自以為了解」直接動作。違反就是 drift 來源。

## Why

LLM 在 vault 工作時最深的盲點是「**不先發現就跳動作**」。表現有 3 層：

| 層 | 行為盲點 | 後果 |
|---|---------|------|
| **行為層** | `Read(path, limit:80)` 部分讀大 CLAUDE.md / 不先 `ls` 探勘新資料夾 / 只讀「自以為相關」的檔 | 拿錯規範、放錯位置、漏看 `_README` |
| **文件層** | CLAUDE.md 沒明寫「ingest 前必讀清單」/ `_` 前綴慣例沒 codify / references/ 沒 hub 頁 | LLM 不知該讀什麼，憑印象瞎找 |
| **SOP 層** | 沒「Discovery before Action」結構性反射 / 沒「不確定就讀全文」default | LLM 直接動手，drift 自然發生 |

→ 規則 O 把 3 層全 codify。**根本原則**：靠規則約束，不靠個別 LLM 自律。LLM 自律在下個 session 就會忘；規則寫進 CLAUDE.md 永遠在 system prompt。

## §O.1 行為層 — Read 工具正確用法

LLM 用 Read 工具時的 default 應該是「**讀全文**」，不是「自我保守加 limit」。Read 工具預設能讀 2000 行，不會因為大就 OOM——LLM 加 limit 是錯誤的自我約束。

### 用法決策表

| 場景 | 該做 | 為什麼 |
|------|------|--------|
| 首次接觸新規範 / 新 hub / 新 entity | **讀全文**（< 500 行直接讀；500-2000 行也直接讀）| 不知道哪段重要，limit 會切到 context |
| 大檔（> 2000 行）| 先 `grep '^## \|^### '` 看 H2/H3 結構 → selective Read 對應段 | Read 工具上限 2000 行 |
| 確認某段（已知 line range）| `Read(offset=N, limit=K)` 精準讀 | 已 know what to read |
| 看 metadata / frontmatter only | `Read(limit:15-20)` | 只要 frontmatter |
| **不確定該怎麼讀** | **讀全文**（default safe） | LLM 自我保守 = drift 主因 |

### 反模式

- ❌ 對未讀過的規範檔加 `limit:80`——會切掉重要 context（譬如 §3.1.1.1 在 line 200+ 而你只讀到 80）
- ❌ 「我大概知道」就跳過 Read——LLM「大概知道」≠ vault 規範現況，文件會 drift
- ❌ Read 結果 < limit 就以為讀完了——`limit:200` 但檔有 1000 行只讀了 1/5
- ❌ 用 grep 取代 Read——grep 出 line numbers 後**必須** Read 該段 context，不能只看 grep 摘要

### 例外（可加 limit）

- 大檔已知結構，只要某段 verify（譬如「verify line 150 含 X」）
- 確認 mtime 或 file size 用 `ls -la`，不必 Read
- chat 內已展示過完整內容，回查時 selective 即可

## §O.2 文件層 — 必讀檔清單 + `_` 前綴 SSOT 慣例

### `_` 前綴 = SSOT（Single Source of Truth）

vault 內 `_` 開頭檔 / 資料夾**不是隨意命名**，是文化慣例：**該位置的 ground truth**。

| `_` 前綴 | SSOT 語意 | 行為 |
|---------|----------|------|
| `_README.md` | 進該資料夾必讀（譬如 `00-Inbox/longform/_README.md`、`40-Resources/<topic>/_README.md`）| **ls 看到立刻讀全文** |
| `_MOC.md` | 該主題的結構索引 hub（Dataview / Map of Content）| **同上** |
| `_skill-staging/` | skill source 編輯區（**不是** plugin 載入點）| 知道改這裡是 source-of-truth |
| `_unsorted/` | 未分類 bucket（暫存區）| 處理時 review 內容 |

→ 看見 `_` 前綴 = LLM 該停下來讀全文。

### 每次 ingest / 維護任務必讀檔基準清單

執行**任何** ingest / cascade / 規範改動前，這份清單**全部讀過**（不加 limit）：

| 檔 | 為什麼必讀 |
|----|----------|
| `CLAUDE.md` | vault 規範主檔（規則 A-O + §3 操作 SOP + §4 entity 格式）|
| `wiki/CLAUDE_versions.md`（若有）| 完整版本歷程（看 vault 規範演進，避免按舊規範動作）|
| `wiki/index.md` 或 landing page | 看 vault 現況 + 最近 ingest 紀錄 |
| `Wiki_維護觸發規則.md` | cascade matrix（每個動作對應改哪些檔）|
| 對應任務的 `wiki/rules/rule-X.md` | 從 CLAUDE.md §10 1-row 速查 follow |
| 對應 domain 的 `_MOC.md` | 該 domain 結構索引（譬如 ingest 某 domain 必讀對應 `_MOC.md`）|
| 對應資料夾的 `_README.md`（若存在）| ls 該資料夾看見 `_README` 就讀 |

→ 不讀 = drift。

## §O.3 SOP 層 — Discovery 三步

任何 ingest / cascade update / 規範改動前**必跑**：

### Step 1：ls 探勘

```bash
ls <目標資料夾>/
```

看見什麼：
- `_README.md` / `_MOC.md` → **立刻讀全文**（SSOT）
- 其他 entity / 檔案 → 看結構分布（資料夾深度、命名 pattern）
- 子目錄 → 必要時 `ls -R` 或 `find <path> -maxdepth 3 -type d`

### Step 2：讀必讀檔（不加 limit）

按 §O.2 清單讀全文：
- CLAUDE.md / 觸發規則 / 對應 rule-X.md / domain `_MOC.md` / target `_README.md`
- 若 > 2000 行先 grep H2/H3 結構再 selective

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
| §O.1 行為層（Read 用法）| 進來時讀全 | 接到任務、開檔讀 |
| §O.2 文件層（`_` 前綴 SSOT + 必讀清單）| 進來時讀對檔 | 知道哪些檔必讀 |
| §O.3 SOP 層（Discovery 三步）| 進來時 + confirm doc drift | 動手前 |
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
- ❌ **用 grep 摘要當完整 reading**——grep 給 line numbers 是 navigation aid，不是 substitute
- ❌ **doc drift 不報告**——看到 doc vs reality 不一致只「自己消化」不 chat 報告，下次 session 又踩同雷

## 例外條款

- 純 chat 對話（不寫檔 / 不動 vault state）→ 可省 Discovery
- 已在當 session 同個任務內讀過必讀檔 + 沒中斷 → 不必重讀（chat context 還在）
- 緊急修補（譬如 lint score 突降需立刻定位）→ 走「grep → 修 → 補 Discovery」反向流程，事後補讀

## Compounding Engineering 體現

規則 O 本身是 [[Compounding Engineering]] 飛輪的範例：

1. **同 root cause 踩 N 次** → 識別 pattern
2. **Codify 進規則** → 寫進 CLAUDE.md / 拆檔 wiki/rules/rule-X.md
3. **下個 session LLM 預設讀進 system prompt** → 不再憑記憶
4. **規則 H 版本歷程紀錄** → 規則自身的演進可追溯

→ 不靠個別 LLM 自律，靠規則系統演進。
