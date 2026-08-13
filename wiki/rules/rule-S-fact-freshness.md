---
title: "規則 S — 事實時效三態（timeless / snapshot / pointer）"
domain: wiki
type: rule
status: stable
created: 2026-08-13
updated: 2026-08-13
tags: [rule, freshness, 時效, lint, entity 品質]
aliases: [規則 S, 事實時效, 時效三態, freshness policy]
---

# 規則 S：事實時效三態

> **每條事實必須是三種合法形式之一：timeless（不會過期）／snapshot（帶日期的觀測）／pointer（指向真理所在）。任何宣稱「現在如何」的敘述都必須帶時間戳。**
> 規範源自 OKM（Open Knowledge Metabolism）的 freshness policy；偵測邏輯需依你的語言重寫（見下方「為何不要直接搬上游 linter」）。

## 為什麼需要（其他品質機制的洞）

vault 既有的品質機制**全在「檔案層」**：

| 既有機制 | 管的是 |
|---|---|
| `status`（draft / stable / deprecated）| 這**份**檔案可不可信 |
| `review_by` | 這**份**檔案何時該重審 |
| 規則 H 版本歷程 | 這**份**檔案改過什麼 |

**沒有任何機制管「句子層」**——結果是：一個 `status: stable` 的 entity 裡，可以躺著一句沒有日期的過期事實，而檔案標記仍顯示 stable、LLM 仍照 §4 的引用規則「放心引用」。

> "This is the sentence that becomes a lie next Tuesday while still reading as truth."
>
> 繁中：「這種句子下週二就成了謊言，卻仍讀起來像真話。」

## 三種合法形式

| 形式 | 範例 | 為何合法 |
|---|---|---|
| **Timeless**（不會衰減）| 「Transformer 用 self-attention（自注意力）」 | 不隨時間改變，免日期 |
| **Snapshot**（帶日期觀測）| 「2026-07-18 觀測：某方案 US$17/月」 | 宣稱的是「**當時**為真」→ **永不過期** |
| **Pointer**（指向真理）| 「價格以官方頁為準：`<來源網址>`（最後觀測 US$17，as of 2026-07）」 | 只存指標 + 觀測戳；值可以爛，指標不爛 |

### ❌ 唯一非法形式

**對揮發性事實的無日期現在式宣稱**：

```
❌ 目前業界良率突破 85%
❌ 現在前十大成分股：某公司 ~58%
✅ 2026-07 觀測：業界良率突破 85%
✅ 良率現況見 <來源網址>（最後觀測 85%，as of 2026-07）
```

## 快慢分界

- **慢事實（wiring）**：7 天以上穩定——系統怎麼運作、誰負責什麼、決策與理由。**這才是 vault 該存的東西。**
- **快事實（meter）**：7 天內會變——即時數量、狀態、餘額、行情、star 數、訂閱價格。**存指標，不存值。**

## How to apply

1. **寫 entity 時**：碰到數字 + 「目前 / 現在」，先判斷是慢事實還快事實。快的就加 `（as of YYYY-MM）`，或改寫成 pointer。
2. **價格 / 行情 / 統計類 entity**：切兩層——「長效結構」段（不放數字）＋「數據快照」段（標查證日）。過期時只重寫後者。
3. **只檢查 `status: stable`**：draft 本來就標示未驗證，不苛求。
4. **日誌類豁免**：`wiki/daily/`、各種 report 目錄本身即 dated container，整份就是 snapshot。

## Lint 檢查（可加進 `wiki/tools/lint.py`）

| 規則 | 級別 | 條件 |
|---|---|---|
| **FRESH-1** | warning | `status: stable` entity 內，同一行同時有「當下標記」（目前／現在／當前／現況／如今）＋「數字直接帶揮發單位」（k／M／萬／億／%／★／star／元／美元／`$`）＋**無時間戳** |
| **FRESH-2** | info | frontmatter `review_by` 日期已過 |

輸出建議獨立成 `stale_claims` / `expired_review_by` 欄位，**不進 score、不當 CI gate**——它是稽核清單，不是門檻。

### 為何不要直接搬上游 linter

上游實作的偵測邏輯**全是英文**：揮發名詞表（deal / ticket / star / user / revenue…）與時態標記（`currently|now|today`、`was|were|had`）都是英文正則。直接拿來掃中文 vault，**抓到 0 筆不代表 vault 乾淨，代表它讀不懂中文**；`word:word` 這類正則還會誤抓 `plugin:reload`、`property:read` 之類的標記法。
→ **規範可移植，工具不可直接用。**

### 中文版的設計取捨

**關鍵：數字必須「直接帶揮發單位」，而不是整行有數字就算。**

| 版本 | 判準 | 精確度 |
|---|---|---|
| v1 | 當下標記 + 揮發詞 + 行內任一數字 | **20%** ❌ |
| v2 | 當下標記 + **數字直接帶單位** + 無戳 | **75%** ✅ |

v1 的噪音來自編號清單的數字（`1.`）、功能名（「最新消息」）、vault 的自我描述。另加負向前瞻（如 `k(?![A-Za-z])`）避免誤匹配 `KB` 之類。**偏精確度、容許少量漏報**——寧可漏抓，不可洗版。

## 相關

- 規則 H（`wiki/rules/rule-H-version-history.md`）— 檔案層版本歷程（本規則補的是句子層）
- 規則 O（`wiki/rules/rule-O-discovery-before-action.md`）— 引用前先驗證（時效是「驗證」的時間維度）
- 經驗法則 5（`wiki/rules/heuristic-5-promote-refinement.md`）— 時效型待解屬「未來型」，不擋 stable

---

← 回到 `CLAUDE.md` §10
