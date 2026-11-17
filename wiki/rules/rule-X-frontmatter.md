---
title: "規則 X：文件屬性（frontmatter）"
type: rule
domain: wiki
status: stable
tags: [rule, frontmatter, 屬性, vault-meta]
created: 2026-11-17
updated: 2026-11-17
aliases: [規則 X, 文件屬性規範, frontmatter 規範]
---

# 規則 X：文件屬性（frontmatter）

> vault 內**新建或被改到**的 `.md` 檔，照所在位置填齊必填屬性（檔頭兩條 `---` 之間那段，Obsidian 叫「屬性」）。
> wiki 頁面各欄的定義仍在 [[CLAUDE]] §4。

## 0. 版本歷程

| 版 | 日期 | 內容 |
|---|---|---|
| v1.0 | 2026-11-17 | 初版。同步自 Vincent5588 規則 X v1.0 的通用部分（維護者自用的寫入檢查 hook、三個資源庫的專屬範本、證據資料夾例外不搬） |

## X.1 屬性表

**共用六欄：title、type、status、tags、created、updated**——X.3 沒列為例外的 `.md` 都要有。

| 位置 | 必填 | 值怎麼挑 |
|---|---|---|
| `wiki/entities/` | 共用六欄＋domain、source | type 限 §4 的 8 種、status 限 draft／stable／deprecated（[[CLAUDE]] §4 原規定） |
| `wiki/maps/`、`wiki/rules/` | 共用六欄＋domain | maps 用 `map`、rules 用 `rule` |
| `00-Inbox/` 裡 AI 寫的提案與草稿 | 共用六欄＋domain、source | type 限 §4 的 8 種；status 寫 `draft`；domain 見 X.2 |
| `40-Resources/` | 共用六欄＋source | type、status 照該資料夾現有的值 |
| 其他（20-Projects、10-Notes、30-Areas、Wiki操作文件、Attachments、`wiki/` 其他、根目錄 `index.md` 與 `新手使用手冊.md`） | 共用六欄 | source 選填；type、status 照該區現有的值 |

`README.md` 與 `_` 開頭的索引檔照所在位置那一列；`00-Inbox/README.md` 算「其他」，不算草稿。

## X.2 每欄怎麼填

| 欄 | 怎麼填 |
|---|---|
| title | 標題，跟檔名一致或更好讀 |
| type | wiki 頁面與收件匣草稿從 §4 的 8 種挑（規劃書、手冊、報表多半是 `artifact`，流程與 SOP 是 `process`）；其他位置照該區已經在用的值 |
| status | wiki 頁面限三種；收件匣草稿寫 `draft`；其他照該區習慣（`active`、`done`…）。不知道就寫 `draft`；**AI 不自己把檔標成 `stable`** |
| tags | 至少一個；`[]` 算沒填 |
| created | 建立日期 `YYYY-MM-DD`。補舊檔時**先找紀錄**：檔內版本歷程第一列、daily 第一次提到、git 歷史；只找得到「最晚那天已經存在」就填那天，旁邊加 YAML 註解寫依據。都找不到才用檔案建立時間——**雲端同步重建過的檔，建立時間是重建那天**，不可盡信。不要猜 |
| updated | 這次改的日期——先查當天日期再寫 |
| domain | 從既有 domain 挑（`ls wiki/entities/`）。收件匣草稿找不到合適的就寫 `待定`，交出時說明；不自己開新 domain |
| source | 內容的根據：網址、`[[素材檔]]`，或「YYYY-MM-DD 與使用者對話」；多個寫成清單 |

## X.3 不查的位置

| 位置 | 為什麼 |
|---|---|
| `wiki/daily/`、個人日記（路徑含 `Daily/`） | 有自己的格式（[[CLAUDE]] §14、日記範本），用 `date:` |
| 00-Inbox 的剪報與技能產出 | `type` 是分流記號（`web-clipping`、`youtube-clipping`、`github-clip`…，[[rule-K-raw-precheck\|規則 K]]），格式照 Web Clipper 範本與各技能；靠 `pending_action`、`supersedes` 認出它們 |
| `50-Archive/` | 封存，不再改 |
| `40-Resources/Templates/` | 範本，屬性是空的佔位 |
| `.claude/skills/` | 技能套件，照技能自己的格式 |
| 根目錄 `CLAUDE.md`、`README.md` | AI 說明書與 GitHub 首頁 |

## X.4 舊檔與作者

- **只管新建的檔和這次改到的檔**。改到舊檔就順手補齊，跟 [[rule-W-mermaid-visual-style|規則 W]] 一樣，不另開補舊檔的工作。
- **作者交出前可以改自己剛建的檔**，含 00-Inbox。
- **說「屬性補齊了」要逐欄列出**（[[rule-T-verification-ledger|規則 T]]）：哪幾欄、各填了什麼。只說「已補上」不算。

## X.5 怎麼檢查

本模板**沒有附自動檢查**。AI 寫完一份檔，自己照 X.1 對一次，交出時逐欄列出（X.4）。想做成寫入當下自動提醒，可以請 AI 用 Claude Code 的 hooks 做——規則寫了 AI 照樣會漏，做成檢查才擋得住。

**管不到**：你在 Obsidian 裡直接新建的筆記（不經過 AI）。那部分靠 `40-Resources/Templates/` 的範本帶上欄位。

## X.6 為什麼

維護者遇過：AI 在收件匣寫了兩份文件，被要求「把屬性寫完整」，它補了標題、日期、標籤、狀態就回報「已補上」，type、domain、source 都沒填。查下來三個缺口：

1. **§4 的必填欄位只管 wiki 頁面**，收件匣的草稿沒有規定——「寫完整」是哪幾欄，沒有定義。
2. **沒有任何檢查**會在補一半時提醒。
3. 說「已補上」時沒有逐欄對照。這條規則 T 本來就有，缺的是一張可以對照的表。

不能整個 vault 套同一組欄位：收件匣的 `type` 已經是剪報流程的分流記號、日誌有自己的格式、範本是空的佔位，硬套會把它們弄壞。所以是一張依位置分的表。

⭐ **要別人「寫完整」，得先有一張寫得出「完整是哪幾欄」的表——沒有表，補一半跟補完看起來一樣。**

## 相關

- [[CLAUDE]] §4（wiki 頁面各欄定義）、§14（daily 格式）
- [[rule-T-verification-ledger|規則 T]]｜[[rule-K-raw-precheck|規則 K]]｜[[rule-W-mermaid-visual-style|規則 W]]
