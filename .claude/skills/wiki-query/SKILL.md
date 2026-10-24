---
name: wiki-query
description: |
  Answer questions using the local wiki/ knowledge base with mandatory
  bidirectional-link citation. Use when the user says: 「我 wiki 裡 X 是什麼」
  「查 wiki」「wiki 裡 X 怎麼說」「knowledge base 找 X」「過去我對 X 的決定」
  「historical decision on X」「query wiki」「/query」.

  ALWAYS reads wiki/index.md first to locate relevant pages, then deep-reads
  matching entities/maps, then synthesizes a response. Every claim must be
  cited with [[wiki-link]] back to the source page. If wiki has no relevant
  content, declare "本地知識庫未找到，以下為通用知識回答" before answering.

  Differs from web search or general LLM recall: this skill enforces
  grounding in YOUR local wiki, not the model's training data.
user-invocable: true
---

# wiki-query 技能

## 核心目標

把使用者的提問轉成「**對本地 wiki/ 的深度檢索 + 雙鏈引用回答**」。
強制把回答錨定在你已編譯的知識上，不靠模型記憶幻覺。

## 觸發場景

- 使用者輸入 `/query <問題>`、`/q <問題>`
- 自然語言：
  - 「我的 wiki 裡關於 X 是怎麼說的」
  - 「過去我對 Y 的決策是什麼」
  - 「查 Z 相關的知識」
  - 「knowledge base 找 X」
  - 「我之前是不是有寫過 X」
- 提及 wiki / knowledge base / 筆記 / 知識庫 等關鍵詞

## 流水線（4 步驟，順序不可顛倒）

### Step 1：永遠先讀 wiki/index.md

```
Read("wiki/index.md")
```

從 index.md 找出與問題相關的：
- 條目（entities/）
- 地圖（maps/）
- log.md 中相關的歷史變更（如使用者問「上次我寫 X 是什麼時候」）

**禁止跳過此步驟** — 即使你「覺得」知道答案。index 是唯一的權威路徑。

### Step 2：深度閱讀候選頁

對 Step 1 找到的每個候選頁：

```
Read("wiki/entities/<page>.md")
```

- 如果頁面有「## 相關概念」連結到其他頁 → 視深度需要也 Read 進來
- 控制：通常 3-5 頁就夠，不要無限延伸
- 大型 entity（>200 行）可用 offset/limit 取相關段

### Step 3：綜合回答（含強制雙鏈引用）

組成答案時，**每個事實點必須標註 `[[頁名]]`**：

```
✅ 良好範例：
「訂單系統的折扣上限（[[折扣上限]]）規定：
 - 訂單帶有促銷標記 → 不得再疊加會員折扣（[[促銷標記 PromoFlag]]）
 - 一般會員 → 折扣上限為 9 折（[[會員等級]]）
 計算邏輯位於 [[PricingService]] 的 CalcDiscountCap 方法。」

❌ 不良：
「訂單系統的折扣上限規則是這樣這樣...」（無引用）
```

### Step 4：回報「答案來自哪裡」

回應結尾固定加：

```
---
📚 引用來源：
- [[頁面 1]]
- [[頁面 2]]
- [[頁面 3]]
🕐 查詢時間：YYYY-MM-DD HH:MM
```

## 降級策略（重要）

### 情況 A：wiki 完全沒有

```
Step 1 讀 index.md → 找不到相關條目
   ↓
回應開頭明確聲明：
「⚠️ 本地知識庫（wiki/）未找到相關內容，以下為通用知識回答：

[後續正常回答，但聲明資訊不在 wiki/ 中]」
```

不要假裝在 wiki 裡找到。

### 情況 B：wiki 有部分

```
Step 1-2 找到 2 個相關頁但不完整
   ↓
回應開頭：
「📍 wiki/ 中有部分相關內容：[[A]]、[[B]]，
  但未涵蓋 [使用者問的某面向 X]。以下整合 wiki 內容 + 通用知識回答：」
```

明確標出哪些靠 wiki、哪些是補的。

## 主動知識固化（進階）

當回答**價值高**且**將來可能再被問**時，主動建議：

```
💡 此回答涵蓋面廣，建議固化為 wiki/entities/<XXX>.md，
   未來查詢可直接讀檔，不必重新綜合。要我建嗎？
```

→ 若使用者同意，呼叫 wiki-ingest 或手動建頁。

## 何時**不**該用 wiki-query

- ❌ 通用知識（「太陽系幾顆行星」）— 直接答即可
- ❌ 即時資料（天氣、股價）— 該用 WebSearch
- ❌ 寫程式（不是查知識）— 該用一般對話
- ❌ 純算數 / 翻譯 — 直接答

→ 觸發語意要明確「跟我的 wiki / 知識庫 / 筆記有關」。

## 跟其他 skill 的區別

| skill | 方向 |
|-------|------|
| **wiki-query** | wiki → 使用者（讀） |
| **wiki-ingest** | raw → wiki（寫單檔） |
| **wiki-compile** | 長文檔 → wiki（寫多檔） |
| **wiki-lint** | wiki 自身（檢查） |
| **wiki-notion-sync** | wiki → Notion（推送） |

→ 4 個寫入 / 檢查 / 推送 + 1 個讀取（wiki-query）= 完整生命週期。

## 範例：用訂單系統的 wiki 問問題

```
你：「訂單退回時要清掉哪些欄位？」

wiki-query 執行：
  1. Read wiki/index.md → 找到 [[退單流程]]
  2. Read wiki/entities/退單流程.md
  3. Read wiki/entities/促銷標記 PromoFlag.md（cross-reference）
  4. 綜合：

回應：
「訂單退回時系統清除以下欄位（出處：[[退單流程]]）：
 1. CurrentStep（客服退回已出貨訂單時不變）
 2. FinalPrice、DiscountAmount、PriceBeforeAdjust（[[金額精度]]）
 3. IsLocked
 4. PromoFlag → 重置為 \"None\"，PromoFlagReason → null（[[促銷標記 PromoFlag]]）
 5. 將 Step >= 退回步驟 的舊 ShipmentRecord 標記為 IsReturned = true

---
📚 引用來源：
- [[退單流程]]
- [[促銷標記 PromoFlag]]
- [[金額精度]]
🕐 查詢時間：2026-04-26 14:30」
```

## 限制

- 依賴 wiki/index.md 的完整度——若 index 漏列頁，query 找不到
- 大 wiki（>500 頁）時 Step 1 可能載入大量 token——這時改 grep 找
- 跨語言查詢（中文問英文 wiki）效果視 model 而定

## 進階：批次查詢

使用者問多個問題時：

```
你：「訂單系統的折扣規則 + 運費規則 + 退款計算 各自是什麼？」

wiki-query 處理：
  並行 grep 三個關鍵字 → 並行 Read 三組相關頁 → 分段回答
  每段都有自己的 [[]] 引用
```

→ 比逐問逐答快 3x。
