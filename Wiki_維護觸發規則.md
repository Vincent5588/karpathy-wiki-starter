---
title: "Wiki 維護觸發規則 — Propagation Matrix"
type: artifact
domain: wiki
status: stable
tags: [wiki, sop, propagation, maintenance, rules]
created: 2026-01-01
updated: 2026-01-01
aliases: [Propagation Matrix, Wiki cascade rules, 連動更新規則]
cssclasses: [wide]
---

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-01-01 | 模板初版（移植自 karpathy-wiki-pattern）|

---

# 🔁 Wiki 維護觸發規則（Propagation Matrix）

> **核心痛點**：vault 內各文件互有版本依賴。改 A 卻忘了 cascade 改 B → A 看起來合理但 B 跟 A 對不上 → 找不到、誤導。本檔列每個常見動作後**必須**改的所有文件，給 LLM 跟使用者雙方都清楚。

> 配套讀物：[[CLAUDE]]（規範）/ [[WIKI_TODO]]（待辦）/ [[wiki/index]]（主目錄）

---

## 📌 設計原則

1. **「強制」級別 vs 「建議」級別**：強制 = 不做的話下次有人讀會被誤導；建議 = 可累積到下次 batch 一起做
2. **每次都跑「自我檢查」清單**：完成動作後 grep / ls 確認已 propagate
3. **歷史記錄不 cascade**：wiki/daily/ 過去日期的記錄是 frozen records，不重寫
4. **stub 機制處理移檔**：移走的檔案原位置留 redirect stub，不破壞歷史路徑連結

---

## 1. Ingest 1+ entity（最高頻動作）

### 🔴 強制更新

| 檔案 | 改什麼 | 為什麼 |
|------|------|------|
| `wiki/entities/<domain>/<type>/<X>.md` | 新建 entity 本體 | 主要產出 |
| `wiki/maps/<X>.md`（若衍生 map）| 新建跨主題地圖 | map 是入口跳板 |
| `wiki/daily/YYYY/MM/YYYY-MM-DD.md` | 加 phase / 一行摘要 / 詳細小節 | 變更日誌 |
| `wiki/index.md` header「最後更新」| 改今天日期 + 一句話描述 | 一眼看到 vault 是不是 alive |
| `wiki/index.md` header「entity 計數」| bump 數字（recursive find）| 規模感 |
| `wiki/index.md` domain section | bump 該 domain 條目 | 新 entity 需要出現在目錄 |

### 🟡 建議更新（當天 batch 一次）

| 檔案 | 改什麼 |
|------|------|
| [[WIKI_TODO]] | 衍生待辦事項、「最後更新」日期 |
| [[Wiki_專有名詞對照表]] | 若新 entity 含**未收錄的英文專有名詞** → 加新 row |
| [[Wiki_儀表板]] | bump「最近動態」+ entity 計數快照 |

### 💬 必做：chat 報告

每次 ingest 完，LLM 在 chat **主動**報告（不必使用者問）：
- 新建幾個 entity，列每個的 `[[wikilink]]`
- 衍生哪些 map
- raw 路由到 PARA 哪邊（若有）
- 哪些更新 checklist 已完成
- 後續待補的 entity（譬如新引用但未建的 stub）

### 🔍 自我檢查（chat 報告前跑）

```bash
VAULT="<vault root>"
echo "今日 daily 是否存在：$(ls $VAULT/wiki/daily/$(date +%Y/%m)/$(date +%F).md 2>&1)"
echo "wiki/index.md 是否提到今天：$(grep -c "$(date +%F)" $VAULT/wiki/index.md)"
echo "entity 總數：$(find $VAULT/wiki/entities -name '*.md' | wc -l)"
echo "map 總數：$(find $VAULT/wiki/maps -name '*.md' | wc -l)"
```

---

## 2. Lint 跑完

### 🔴 強制更新

| 檔案 | 改什麼 |
|------|------|
| `wiki/reports/LINT/YYYY/MM/LINT_<TS>.json` | 原始輸出（lint.py 自動寫）|
| `wiki/daily/YYYY/MM/YYYY-MM-DD.md` | 一行紀錄「Lint Score N/100」+ 主要問題摘要 |
| `wiki/PROGRESS.md` | 「系統健康狀態」區塊的 Lint Score 數字 |
| [[Wiki_健康度監控]] | 追加一 row（時點 / Score / Orphans / Missing / God / Collisions / 觸發事件）|

### 🟡 建議更新

| 檔案 | 改什麼 |
|------|------|
| [[WIKI_TODO]] | High Priority 修補項加入 todo |
| [[Wiki_儀表板]] | 「健康狀態快照」table 數字同步 |

### 💬 chat 報告

- Score 對比上次（漲 / 跌 / 持平）
- High Priority 問題清單（給使用者選擇要不要 repair）
- False positive 標記（譬如特殊格式連結被誤判為 missing）

---

## 3. Repair 套用

### 🔴 強制更新

| 檔案 | 改什麼 |
|------|------|
| `wiki/reports/REPAIR/YYYY/MM/REPAIR_<TS>.md` | dry-run + apply audit |
| 受影響 entity（多個）| 修補（加 backlink / 補 stub / 刪除 / merge）|
| `wiki/daily/YYYY/MM/YYYY-MM-DD.md` | 一行「修補 N 條，影響 M entity」|
| `wiki/PROGRESS.md` | Lint Score 如有變化同步更新 |

### 💬 chat 報告

- dry-run plan 給使用者批准（規則 E：show before write）
- apply 後實際結果（成功 N / 失敗 M）

---

## 4. status 變動（Promote / Deprecate）

### 🔴 強制更新

| 檔案 | 改什麼 |
|------|------|
| 受影響 entity frontmatter `status:` | draft → stable 或 → deprecated |
| 受影響 entity 內文 | 若 deprecated，加「## ⚠️ Deprecated」區塊 |
| `wiki/daily/YYYY/MM/YYYY-MM-DD.md` | 一行「N entity 升 stable / M entity 改 deprecated」|

### 🟡 archive / delete 場景（極少數）

| 動作 | 條件 | 強制 |
|------|------|------|
| Archive 移到 `wiki/_archive/` | deprecated + 6 月無查詢 | 留 git history、寫 daily log |
| Delete（git rm） | deprecated + 12 月無查詢 | **show before write**（規則 E），daily log 必須記錄判斷依據 |

→ archive / delete 詳細 SOP + 追蹤表見 [[Wiki_刪檔處理SOP]]。任何刪檔動作必依該 SOP 走「Active → 50-Archive → 30 天 → Delete」三層緩衝期。

---

## 5. 改 CLAUDE.md（規範變動）

### 🔴 強制 cascade

| 檔案 | 何時改 |
|------|------|
| `CLAUDE.md` 自身 §0 版本歷程表 | 永遠加新 row |
| `CLAUDE.md` 自身 header version | bump（小改 patch / 大改 minor）|
| `wiki/PROGRESS.md` | 若規範影響 session 熱身流程 |
| [[Wiki_維護觸發規則]]（本檔）| 若新規範改變 cascade 邏輯 |

### 🟡 建議 cascade

| 情境 | 對應檔案 |
|------|---------|
| 加新規則（A-Z 系列）| 影響哪些 skill 的操作流程 → 補規範 |
| 改既有規則的措辭 | grep 全 vault 找引用該規則的文件，cascade 改 |
| 加新規則 + 內容 ≥ 30 行 | 直接拆 `wiki/rules/rule-X.md`（規則 L），主檔只留 1-row 速查 |
| 規則 J / D 譯名相關變動 | 同步檢查 [[Wiki_專有名詞對照表]] 是否需要更新 |
| 規則 K Step 0 預檢分流邏輯變動 | 同步檢查 [[Wiki_Web_Clipper_範本]] frontmatter `pending_action` 值 |

### 💬 自我檢查

```bash
grep -rn "v1\.X" $VAULT --include='*.md' | grep -v daily/  # 找所有提到舊版本的地方
```

---

## 6. Vault 入口頁改動

若你的 vault 有入口頁（如 `Welcome.md` 或 `README.md`），更新它時：

### 🔴 強制 cascade

| 檔案 | 何時改 |
|------|------|
| 入口頁自身 | 主要改處 |
| `wiki/PROGRESS.md` | 若 PROGRESS 也提及入口頁的 plugin 版本 |

---

## 7. Plugin 升版（vX.Y 跳一級）

### 🔴 強制 cascade

| 檔案 | 改什麼 |
|------|------|
| `CLAUDE.md` | §0 版本歷程加新 row、skill 對照表更新 |
| `wiki/PROGRESS.md` | 「Plugin 版本」欄位 |
| 各 skill 內 `SKILL.md` | `version:` 欄位 |

### 🟡 建議

| 檔案 | 改什麼 |
|------|------|
| [[Wiki_維護觸發規則]]（本檔）| 若新增 skill 改變動作觸發點 |

---

## 8. 檔案搬遷（移檔 / 改名）

### 🔴 強制動作

1. **複製**到新位置先建（不直接 mv，避免 sync 問題）
2. **原位置改成 redirect stub**（保留 frontmatter `moved_to: [[新名]]` + 內文一句話導向）
3. **cascade-edit active files** 內所有 `[[舊]]` → `[[新]]`
   - active files = CLAUDE.md + wiki/maps/* + wiki/entities/* + wiki/index.md
4. **wiki/daily/ 歷史不動**（frozen records，靠 stub redirect 保留可達性）
5. **`wiki/daily/YYYY/MM/YYYY-MM-DD.md`** 加當日紀錄

### ⚠️ 永遠不要

- 直接刪除原檔（破壞歷史連結）
- 跳過 cascade-edit（active files 連結會壞）
- 改 entity 的 basename 卻不留 stub（[[wikilink]] 全壞）

---

## 9. 常見「忘記更新」陷阱

| 場景 | 反例 | 正例 |
|------|------|------|
| 大批 ingest 後 | 只更新 entity 沒動 wiki/index.md + PROGRESS.md | 每次 ingest 完跑 §1 強制更新 checklist |
| 改 CLAUDE.md 規則 | 只改 CLAUDE.md，本檔沒同步 | 規範改完 grep 引用該規則的所有檔，逐一更新 |
| Plugin 升版 | 只重打包 .plugin，沒改 PROGRESS.md | 升版 SOP 含 cascade checklist（本檔 §7）|
| 移動 wiki/index.md | 沒留 stub，daily log 連結變紅色 | 規則 §8：永遠留 redirect stub |
| 改一個 entity | 只改一頁，但多個 entity 引用它 | grep entity basename 找全部 cross-link，逐一 review |

---

## 10. LLM agent 接手時的「先看本檔」規範

新 session 開始 / 新 agent 進入 vault 時：

1. **先看 CLAUDE.md** — 規範
2. **次看本檔** — 動作 → cascade matrix
3. **執行動作前**：在 chat 自述「我要做 X，依本檔規則 §N 我會 cascade 更新 [清單]」
4. **完成後**：在 chat 報告每個 cascade 點是否已做
5. **不確定時**：問使用者，不要自己決定要不要 cascade

---

## 11. 觸發詞速查（給使用者用）

| 你說 | 觸發 cascade matrix 哪一節 |
|------|---------------------|
| 「ingest X」 / 「處理 X」 | §1 |
| 「巡 wiki」 / 「lint」 | §2 |
| 「修 wiki」 / 「repair」 | §3 |
| 「批次升 stable」 / 「審草稿」 | §4 |
| 「改 CLAUDE 加新規則」 | §5 |
| 「打包 plugin」 / 「升版到 vX.Y」 | §7 |
| 「把 X 移到別的位置」 / 「rename Y」 | §8 |

---

## 12. 觸發本檔 cascade 的條件

當 CLAUDE.md 加新規則 / 新動作類型 / 新 skill 時，本檔本身也需要更新：

- 加新動作（譬如加新 skill）→ 加新 §N
- 改 cascade 邏輯 → 改對應節
- 加新「忘記更新」陷阱 → 加 §9 row

→ 本檔自己就是「meta-規範」，跟 CLAUDE.md 互補：CLAUDE.md 講「應該怎麼做」，本檔講「做完該動哪些檔」。

---

## 相關

- [[CLAUDE]] — vault 主規範
- [[WIKI_TODO]] — 待辦清單
- [[wiki/index]] — wiki 主目錄
- [[wiki/PROGRESS]] — 系統健康狀態

← 回到 [[wiki/index]]
