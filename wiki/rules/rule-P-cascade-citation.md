---
title: "規則 P：Cite-or-Die Cascade Citation"
tags: ["claude-md-rule", "rule-P", "cascade", "propagation", "accountability", "llm-discipline"]
domain: wiki
type: rule
status: stable
maintained_by: LLM
parent: "[[CLAUDE]] §10"
created: 2026-05-12
updated: 2026-05-12
aliases: [規則 P, Cite-or-Die, Cascade Citation]
---

## 0. 版本歷程

| 版本 | 日期 | 主要變動 |
|------|------|---------|
| v1.0 | 2026-05-12 | 初版——從同 root cause「沒讀觸發規則就跳動作」連環踩 cascade 漏更新 codify。**根本原則**：把「我可能跳過 [[Wiki_維護觸發規則]]」變成 chat 中明顯 caller-verifiable 的動作 |

# 規則 P：Cascade 前必引用觸發規則 §N（Cite-or-Die）

> **核心鐵則**：任何 vault 寫入動作前，LLM **必須**在 chat 引用 [[Wiki_維護觸發規則]] 對應 §N 的具體 cascade 清單。若無法引用 → 證明沒讀過觸發規則 → 必須停下來讀，才能繼續。

## Why

LLM 在 vault 工作時反覆踩的雷：**知道要做 X，但漏掉 cascade 該動的索引 / 監控檔**。常見場景：

- ingest 完 entity 但漏更 Wiki_儀表板 / Wiki_健康度監控 frontmatter
- 補既有 stable entity 卻漏 Wiki_主目錄「最近 ingest」紀錄
- Plugin 升版漏更 Welcome / 維護實戰手冊版本號

**Root cause**：CLAUDE.md ⚡ section 寫「⚠️ 新 session 開始必讀 [[Wiki_維護觸發規則]]」是**被動文字**——沒有任何機制阻止 LLM 跳過，跳過後使用者也看不出來。

**設計理念**：把「我可能跳過」變成 **chat 中明顯 caller-verifiable 的動作**。
要嘛 chat 中有「依 [[Wiki_維護觸發規則]] §N，本次將 cascade：①② ...」引用 + cascade 清單，要嘛沒有（= 證明沒讀過觸發規則）。

**規則三角閉環**（v1.0 codify 完成）：

| 規則 | 紀律維度 |
|---|---|
| 規則 E（show before write） | output 紀律：寫前先 show |
| 規則 O（Discovery Before Action） | input 紀律：執行前先探勘 |
| **規則 P（本規則）** | **process 紀律：cascade plan 寫出來給 caller 看** |

→ input + output + process 三層 verifiable 紀律完整。

## 觸發條件

凡是 vault 寫入動作前一律 cite：

- 新建 entity（atomic 或 atomize:false 都算）
- 補既有 entity（heuristic 2）
- Lint 跑完寫 trend / dashboard
- Repair 套用
- Status 變動（promote / deprecate / archive / delete）
- 改 CLAUDE.md / 規範文件
- Plugin 升版
- 移檔 / rename / 改 basename

## 引用格式

```
依 [[Wiki_維護觸發規則]] §N，本次「<動作描述>」將 cascade：
 ① <檔案 1>（強制 / 建議）— <一句話原因>
 ② <檔案 2>（強制 / 建議）— <一句話原因>
 ...
 → 自我檢查：`<驗證 bash 指令>`
```

### 範例 A：ingest 1 個新 atomic entity

```
依 [[Wiki_維護觸發規則]] §1，本次「ingest [[X]] 到 <domain>/<type>/」將 cascade：
 ① wiki/entities/<domain>/<type>/X.md（強制 — 新建本體）
 ② wiki/daily/YYYY/MM/YYYY-MM-DD.md（強制 — daily log）
 ③ Wiki_主目錄「📥 最近 ingest 紀錄」+「📅 最後更新」+ domain 計數 +
    entity 總數（強制 × 4）
 ④ wiki/最新資料歷史/YYYY/YYYY-MM.md（強制 — ingest history hub）
 ⑤ Wiki_儀表板 frontmatter `updated:` + 今日 H3（強制）
 ⑥ Wiki_健康度監控 frontmatter `updated:`（強制）
 ⑦ Wiki_專有名詞對照表（建議 — 若有新英文專有名詞）
 ⑧ WIKI_TODO（建議 — 衍生待辦）
 ⑨ PARA routing raw（強制 — 提案 + 等批准 + 搬檔）

 自我檢查：
   find wiki/entities -name '*.md' | wc -l           # entity 總數
   grep -c "$(date +%F)" Wiki_主目錄.md                # 主目錄今日提及
   grep -l "updated: $(date +%F)" Wiki操作文件/Wiki_*.md  # 監控檔 frontmatter bump
```

### 範例 B：補既有 stable entity（heuristic 2）

```
依 [[Wiki_維護觸發規則]] §1 + [[heuristic-2-second-source|heuristic 2]]：

本次「補既有 [[Y]]（<domain>/<type>, stable）」將 cascade：
 ① wiki/entities/<domain>/<type>/Y.md（強制 — 補 source / 內容 / 規則 H 版本歷程）
 ② wiki/daily/...（強制）
 ③ Wiki_主目錄「📥 最近 ingest」+「📅 最後更新」（強制 × 2，計數不變）
 ④ wiki/最新資料歷史/YYYY/YYYY-MM.md（強制 — 補既有也算 ingest history）
 ⑤ Wiki_儀表板 frontmatter（強制）
 ⑥ Wiki_健康度監控 frontmatter（強制）

 ⚠️ 補既有跟新建唯一差別：domain 計數 + entity 總數不變；其他 cascade 全做。
```

## 違規偵測

| 信號 | 結論 |
|---|---|
| Chat 中沒看到「依 [[Wiki_維護觸發規則]] §N」引用 | LLM 沒讀觸發規則 → 違反規則 P |
| 引用了 §N 但 cascade 清單明顯短於 §N 規定 | LLM 讀了但偷工 → 違反規則 P |
| Cascade 做完 daily log 沒寫「自我檢查」結果 | 自我檢查跳過 → 部分違反 |

使用者隨時可在 chat 喊「**規則 P check**」要求 LLM 列出當前已 cascade 完的清單 vs 應 cascade 清單 diff。

## 跟其他規則的關係

| 規則 | 對比 |
|---|---|
| 規則 E（show before write） | E 講「寫前提案」；P 講「提案內容**必含** cascade plan + §N 引用」。**P = E 的具體化** |
| 規則 O（Discovery Before Action） | O 講「執行前 discovery」；P 講「discovery 完把 cascade plan **寫出來**讓 caller 看到」。**P = O 的 output 紀律** |
| 規則 M.1（Reality Checker / NEEDS WORK） | P 是執行紀律的 verifiable handle —「我說我做了」vs「chat 中有 cite 證據」 |
| 規則 L（拆檔規範） | 規則 P 自身 > 30 行 → 拆檔（本檔即實踐） |
| 規則 H（版本歷程） | 重大 cascade 動作日 daily log 寫進「自我檢查 audit」段也算規則 H 精神延伸 |

## 例外

下列場景**不需** cite §N：

- 純 chat 對答（不寫檔）
- 對沙箱 / 暫存目錄寫檔（不影響 vault）
- 使用者在同 session 明確說「直接做不必 cite」/「直接改」

## 配套（v1.7+ 起）

1. **CLAUDE.md ⚡ 新 session 熱身** 列入「規則 P」必讀提醒
2. **wiki-ingest skill staging Step 0** 自動觸發規則 P 引用（plugin v1.4.5+）
3. **lint.py cascade 完整性檢查** 偵測「daily 提到 ingest 但 Wiki_儀表板 / Wiki_健康度監控 frontmatter 沒同日 / 之後 bump」→ 標 🔴 incomplete cascade

## 觸發契機（generic 描述）

維護者連環踩同類雷：知道 [[Wiki_維護觸發規則]] 存在卻沒讀，導致 ingest 後漏 4 個強制 cascade；補既有時連 Wiki_主目錄 都漏。使用者反問「Wiki_維護觸發規則 你沒有看這個嗎？」直球點破——確認「必讀」被動文字不能依賴 LLM 自律，需要 **chat-verifiable 紀律機制**。規則 P 即此設計。

## 相關

- [[Wiki_維護觸發規則]] — cascade matrix（本規則的引用對象）
- [[rule-E-show-before-write|規則 E]] — 提案紀律
- [[rule-O-discovery-before-action|規則 O]] — 探勘紀律
- [[rule-M-execution-philosophy|規則 M]] — 執行紀律
- [[rule-L-self|規則 L]] — 規範拆檔
- [[CLAUDE]]
