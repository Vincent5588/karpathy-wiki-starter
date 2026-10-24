---
name: wiki-status-promote
description: 批次審查並提升 wiki/entities/ 內 status=draft 的 entity 到 stable / 改 deprecated / 留 draft（加 review_by 提醒日期）。當使用者說「批次升 stable」「審草稿」「promote drafts」「lint 完幫我升 stable」「全部 draft 過一遍」時，立即啟動此 Skill。內建 show-before-write 原則：每筆動作前必先在對話中提案 → 等使用者批准 → 才動 frontmatter。配合 [[Compounding Engineering]] 飛輪：每批升 stable 結束時自動詢問是否有規律可寫進 vault CLAUDE.md。
---

# wiki-status-promote

## 為什麼存在

vault 在持續 ingest 過程中會累積大量 status=draft 的 entity。這個狀態原本是品質訊號（「還沒驗證 / 還沒被引用 / 還在發酵」），但時間久了會變成**訊號被噪音淹沒**——65 個 draft 裡，可能其實 30+ 已經穩定可升 stable。

過去做法：手動一個一個改 frontmatter，**每次 30-45 分鐘很煩**，多數人不會做，draft 就無限累積。

`wiki-status-promote` 把這件事**結構化 + 批次化 + 互動化**——每筆 LLM 給初步建議、使用者快速 yes/no/skip。同時利用這個機會做 [[Compounding Engineering]]：每批升 stable 都會問「過程中有什麼規律」，把規律寫回 vault CLAUDE.md。

## 觸發詞

| 使用者說 | 啟動 Mode |
|---------|---------|
| 「批次升 stable」 | Quick |
| 「promote drafts」 | Quick |
| 「審草稿」 | Triage |
| 「全部 draft 過一遍」 | Full |
| 「lint 完幫我升 stable」 | Lint-aware（先讀 lint 報告） |

## 三個 Mode

### Mode Quick（保守）

只看符合下列**全部**條件的 draft：

- `created` > 30 天前
- 至少 1 個 inlink（`length(file.inlinks) >= 1`）
- 沒有 `## ⚠️` / `## 待解` / `## 矛盾` 等警示標記

→ 高度自信能直接升 stable 的清單。批量小、決策快。

### Mode Triage（推薦）

對全部 draft 分三類：

- 🟢 **建議升 stable**（同 Quick 條件）
- 🟡 **建議留 draft**（內容完整但 inlinks=0 → 補 backlink 後再升 / 含待解區塊）
- 🔴 **建議改 deprecated**（內容單薄 + 沒被引用 + 創建超過 60 天）

→ 一次走完所有 draft，分桶後逐桶處理。

### Mode Full（嚴格）

全部 draft 一筆一筆過，不做自動分類。適合**首次大整理**或**定期月度健檢**。

## 標準工作流（5 步）

依 [[CLAUDE]] §10 規則 E（show-before-write）執行：

### Step 1｜篩選候選

跑 dataview（pure SQL，不依賴 dataviewjs）：

```dataview
TABLE WITHOUT ID
  file.link AS "頁面",
  domain,
  type,
  date(today) - date(created) AS "存在天數",
  length(file.inlinks) AS "inlinks",
  updated
FROM "wiki/entities"
WHERE status = "draft"
SORT domain, length(file.inlinks) DESC
```

或跑 `promote.py` 取得結構化 JSON（含 entity 一句話定義摘要）。

### Step 2｜分類提案

依當前 mode，對每個候選給建議：

| 信號 | 建議分類 |
|------|---------|
| inlinks ≥ 3 + 90 天沒大改 + 無警示標記 | 🟢 升 stable |
| inlinks 1–2 + 內容完整 + 無待解 | 🟢 升 stable |
| inlinks = 0 但內容完整 | 🟡 留 draft + 補 backlink |
| 含 `## 待解 / 矛盾` 區塊 | 🟡 留 draft（直到裁決） |
| inlinks = 0 + 內容單薄（< 200 字）+ 創建 > 60 天 | 🔴 改 deprecated |
| source 已 routing 但 entity 未 sync | 🟡 先 sync source 再考慮 |

詳見 `references/PROMOTE_RULES.md`。

### Step 3｜批次提案（show-before-write）

按 domain 分組，每筆呈現格式：

```
[N] [[Entity 名]]                            🟢 建議升 stable
   domain/type · created N 天前 · inlinks=M · last update YYYY-MM-DD
   📝 一句話定義（從 entity 第一段 blockquote 抓）
   🔗 主要 backlink: [[X]], [[Y]]
   理由：inlinks ≥ 3 + 內容完整 + 無警示
   動作：[ENTER] 接受 / [s] skip / [k] keep draft / [d] deprecate
```

使用者可：
- **逐筆審**：一個一個按
- **批准全部 🟢**：一句話「都 OK」 → 全部建議升 stable 的批准
- **修改建議**：「第 3 筆改 keep draft」

### Step 4｜執行批准的動作

對 user 確認的：

| 動作 | frontmatter 變動 |
|------|------------------|
| 升 stable | `status: draft → stable`、bump `updated` 為今日 |
| 改 deprecated | `status: draft → deprecated`、加 `## ⚠️ Deprecated` 區塊（含原因 + 替代 entity 連結，如有）|
| 留 draft + review_by | 加 `review_by: YYYY-MM-DD`（90 天後） |
| 跳過 | 不變 |

### Step 5｜寫 log + Compounding 飛輪

#### 5a 寫 wiki/log.md（一行）

```
| YYYY-MM-DD | Status Promote | wiki-status-promote Mode-X | N stable / M draft / K deprecated | （簡短備註） |
```

#### 5b 寫 wiki/daily/YYYY/MM/YYYY-MM-DD.md（詳細）

按 domain 列每筆動作 + 升 stable 的 backlink 完整性 / 升 deprecated 的原因 / 留 draft 的 review_by。

#### 5c Compounding 飛輪（**最重要的一步**）

跑完問使用者：

> 「這次升 stable 過程中，發現什麼可以記進 vault CLAUDE.md 的規律？例如：
>
> - 某類 entity 通常 inlinks 少但很重要（不能只看數字）
> - 某種寫法的 entity 很容易升 stable
> - 某種命名/結構的 entity 都該被 deprecate
>
> 沒觀察到也 OK，跳過。」

如有規律 → 把規律寫進 vault CLAUDE.md §10 個人風格偏好區，**永久變成下次 promote 時 LLM 的判斷依據**。這就是 [[Compounding Engineering]] 在 PKM 上的實作。

## 反模式（skill 內建守門）

- ❌ **一鍵 promote-all**：絕對不接受「全部升 stable」這種粗暴指令——必須經過分類提案
- ❌ **只看 inlinks 數字**：業務規則類常常 inlinks 少但很關鍵（如 [[折扣上限]]）；建議邏輯內建例外
- ❌ **忽略 `## 待解 / 矛盾` 標記**：這是「不要碰」的信號，自動歸類 🟡
- ❌ **不寫 log**：升 stable 是 vault 重要狀態變化，必須留 audit trail
- ❌ **跳過 Compounding 飛輪步驟**：這是 skill 的**核心 value-add**，不能省

## 跟其他 wiki-* skill 的搭配

```
wiki-ingest（建 draft）
    ↓ 累積
wiki-lint（找問題）
    ↓ 健檢
wiki-repair（修可自動修的）
    ↓ 修復
wiki-status-promote（本 skill — 升熟成的）
    ↓ 變 stable
wiki-query（用 stable 知識答問題）
```

→ 補完 entity 生命週期。理想的月度健檢流程：

1. `wiki-lint` → 看健康度報告
2. `wiki-repair` → 修自動可修的
3. **`wiki-status-promote` → 升熟成的 / 改廢棄的**
4. lint 重跑 → 確認健康度提升

## 第一次跑（針對當前 vault 狀態）

vault 目前 status=draft = 65 個（占 37%），燈號 🔴。第一次跑建議：

- **Mode = Triage**（一次走完不漏）
- **分批處理**：按 domain（orders → claude → productivity → travel → wiki → helpdesk）
- **預估時間**：30-45 分鐘
- **預期結果**：30-40 升 stable / 10-15 留 draft / 10-15 改 deprecated 或 merge → draft 比例降到 < 15%（🟢 健康）

跑完後 [[wiki/maps/Wiki 儀表板]] 燈號會從 🔴 變 🟢。

## References

- `references/PROMOTE_RULES.md` — 決策邏輯詳細規則
- `references/PROMOTE_TEMPLATE.md` — 提案訊息標準格式
- `promote.py` — 候選清單產生器（pure Python、不依賴 dataview）

## 跟 vault CLAUDE.md 規則的對應

- **規則 E**（show-before-write）：本 skill 每個動作前都會先提案
- **規則 D**（英文 quote 翻譯）：升 deprecated 的 `## ⚠️ Deprecated` 段若引英文要翻譯
- **規則 A**（raw/ 唯讀）：本 skill 完全不碰 raw/，只動 wiki/entities/

← 回到 [[CLAUDE]]
